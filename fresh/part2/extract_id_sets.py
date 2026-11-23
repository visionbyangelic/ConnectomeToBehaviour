"""
Part 2 -- neuron identity extraction (the Part 1 gate obligation).

Where do the model's neuron populations actually live? Not in model.py.
model.py is a bare engine: it takes lists of FlyWire IDs from whoever calls
run_exp(). The populations used by the published experiments are written out
as literal ID lists inside the two upstream notebooks (example.ipynb and
figures.ipynb). This script extracts them from there.

How it works, and why it is done this way:

1. The notebooks are read as TEXT (they are JSON files) and the ID lists are
   pulled out with pattern matching. Nothing upstream is executed -- no
   importing model.py, no running notebook cells, and sez_neurons.pickle is
   never loaded (a pickle is executable code, and its contents cannot be
   read as text; the SEZ sets that live only in that file are recorded as a
   gap in PART2-ID-SETS.md, not extracted here).

2. Every population is cross-checked two independent ways, as the gate
   obligation requires:
   a. against my old build's constants (src/brain/constants.py), which were
      written separately, from the paper -- if the two transcriptions of the
      same lists disagree anywhere, that is a discrepancy to record;
   b. against the v630 materialisation itself: every extracted ID must be
      present in the completeness file, and the connectivity file's
      index columns must map back onto the same FlyWire IDs the completeness
      file assigns to those row positions (model.py trusts that mapping
      silently; here it is verified for all 14.7M edges).

3. The results are saved as versioned artefacts (one CSV per population plus
   a manifest) so later parts cite the files, not this script's output.

Run with the pinned brain env:
    envs/brain/bin/python repo/fresh/part2/extract_id_sets.py
"""

import hashlib
import json
import re
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

# --------------------------------------------------------------------------
# Paths. Everything is anchored to the connectome-work folder so the script
# behaves the same no matter where it is called from.
# --------------------------------------------------------------------------
WORK = Path.home() / "workspace" / "connectome-work"
UPSTREAM = WORK / "upstream"                      # philshiu/Drosophila_brain_model, read as text only
OLD_CONSTANTS = WORK / "repo" / "src" / "brain" / "constants.py"
DATA = WORK / "repo" / "data"                      # the hashed Part 1 downloads
OUT = Path(__file__).parent / "id_sets_v1"         # versioned artefacts land here

PATH_COMP = DATA / "2023_03_23_completeness_630_final.csv"
PATH_CON = DATA / "2023_03_23_connectivity_630_final.parquet"

# The populations the published experiments use, by the names the notebooks
# give them. `ids_mn9` / `id_mn9` / `id_*` are single neurons or pairs, the
# `neu_*` names are lists.
LIST_NAMES = [
    "neu_sugar", "neu_sugar_left", "neu_bitter", "neu_water", "neu_ir94e",
    "neu_JON_CE", "neu_JON_F", "neu_JON_D_m",
]
SINGLE_NAMES = ["id_mn9", "id_DN1_1", "id_DN2_l", "id_aBN1", "three_inhibitory", "ids_mn9"]

# Friendly artefact names for each notebook name.
PRETTY = {
    "neu_sugar": "sugar_grn_right",
    "neu_sugar_left": "sugar_grn_left",
    "neu_bitter": "bitter_grn",
    "neu_water": "water_grn",
    "neu_ir94e": "ir94e_grn",
    "neu_JON_CE": "jon_ce",
    "neu_JON_F": "jon_f",
    "neu_JON_D_m": "jon_d_m",
}

# Which old-build constant should equal which notebook list (cross-check a).
OLD_BUILD_EQUALS = {
    "neu_sugar": "SUGAR_GRNS_RIGHT",
    "neu_sugar_left": "SUGAR_GRNS_LEFT",
    "neu_bitter": "BITTER_GRNS",
    "neu_water": "WATER_GRNS",
}


def sha256_of(path):
    """Hash a file the same way Part 1 recorded its hashes."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def notebook_sources(nb_path):
    """Return the source text of every code cell in a notebook.

    A .ipynb file is JSON; reading it as text executes nothing.
    """
    nb = json.loads(Path(nb_path).read_text())
    return ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]


def find_lists(sources, name):
    """Find every `name = [ ... ]` definition in the cell sources.

    Returns a list of (cell_number, [ids]) -- a population defined in several
    places must come out identical everywhere, which the caller checks.
    """
    found = []
    pat = re.compile(rf"^{name}\s*=\s*\[(.*?)\]", re.M | re.S)
    for cell_no, src in enumerate(sources):
        for m in pat.finditer(src):
            ids = [int(x) for x in re.findall(r"7205759406\d{8}", m.group(1))]
            found.append((cell_no, ids))
    return found


def find_singles(sources, name):
    """Find every `name = 720...` (or `name = [720..., 720...]`) assignment."""
    found = []
    pat = re.compile(rf"^{name}\s*=\s*(\[?[0-9,\s\]]*7205759406\d{{8}}[0-9,\s\]]*)\]?", re.M)
    for cell_no, src in enumerate(sources):
        for m in pat.finditer(src):
            ids = [int(x) for x in re.findall(r"7205759406\d{8}", m.group(1))]
            if ids:
                found.append((cell_no, ids))
    return found


def parse_old_constants():
    """Pull the ID lists out of my old build's constants.py, as text."""
    text = OLD_CONSTANTS.read_text()
    out = {}
    for name in ["SUGAR_GRNS_RIGHT", "SUGAR_GRNS_LEFT", "BITTER_GRNS", "WATER_GRNS"]:
        m = re.search(rf"^{name}\s*=\s*\[(.*?)\]", text, re.M | re.S)
        out[name] = [int(x) for x in re.findall(r"7205759406\d{8}", m.group(1))]
    for name in ["MN9_LEFT", "MN9_RIGHT", "DN1_1", "DN2_L"]:
        m = re.search(rf"^{name}\s*=\s*(7205759406\d{{8}})", text, re.M)
        out[name] = int(m.group(1))
    return out


def main():
    report = {"populations": {}, "checks": {}, "discrepancies": []}

    # ------------------------------------------------------------------
    # Step 1: extract from both notebooks, and require that repeated
    # definitions of the same list agree with each other exactly.
    # ------------------------------------------------------------------
    sources = {
        "example.ipynb": notebook_sources(UPSTREAM / "example.ipynb"),
        "figures.ipynb": notebook_sources(UPSTREAM / "figures.ipynb"),
    }
    all_sources = sources["example.ipynb"] + sources["figures.ipynb"]

    extracted = {}   # notebook name -> list of ids (the agreed definition)
    for name in LIST_NAMES:
        defs = find_lists(all_sources, name)
        if not defs:
            report["discrepancies"].append(f"{name}: no definition found in either notebook")
            continue
        first = defs[0][1]
        for cell_no, ids in defs[1:]:
            if ids != first:
                report["discrepancies"].append(
                    f"{name}: definition in cell {cell_no} differs from the first "
                    f"({len(ids)} vs {len(first)} ids)")
        extracted[name] = first
        report["populations"][PRETTY[name]] = {
            "notebook_name": name, "n_definitions_found": len(defs),
            "count": len(first), "duplicates_within_list": len(first) - len(set(first)),
        }

    for name in SINGLE_NAMES:
        defs = find_singles(all_sources, name)
        if not defs:
            report["discrepancies"].append(f"{name}: no assignment found in either notebook")
            continue
        first = defs[0][1]
        for cell_no, ids in defs[1:]:
            if ids != first:
                report["discrepancies"].append(
                    f"{name}: assignment in cell {cell_no} differs ({ids} vs {first})")
        extracted[name] = first

    # MN9: the pair, in the notebooks' stated order (left, right).
    mn9 = extracted.get("ids_mn9") or extracted.get("id_mn9")
    report["populations"]["mn9"] = {
        "notebook_name": "ids_mn9", "count": len(mn9),
        "left": mn9[0], "right": mn9[1] if len(mn9) > 1 else None,
        "note": "order as written in figures.ipynb cell 17: '# left and right'",
    }
    # The descending-neuron readouts of the JON experiments, plus aBN1.
    report["populations"]["adn1"] = {"notebook_name": "id_DN1_1", "count": 1,
                                     "ids": extracted.get("id_DN1_1")}
    report["populations"]["adn2_left"] = {"notebook_name": "id_DN2_l", "count": 1,
                                          "ids": extracted.get("id_DN2_l")}
    report["populations"]["abn1"] = {"notebook_name": "id_aBN1", "count": 1,
                                     "ids": extracted.get("id_aBN1")}
    report["populations"]["three_inhibitory"] = {
        "notebook_name": "three_inhibitory", "count": len(extracted.get("three_inhibitory", [])),
        "ids": extracted.get("three_inhibitory"),
        "note": "the three inhibitory neurons silenced in the JON-F experiment (figures.ipynb cell 70)",
    }
    # JON all, exactly as upstream constructs it: CE + F + D_m.
    jon_all = extracted["neu_JON_CE"] + extracted["neu_JON_F"] + extracted["neu_JON_D_m"]
    extracted["neu_JON_all"] = jon_all
    report["populations"]["jon_all"] = {
        "notebook_name": "neu_JON_all (= CE + F + D_m)", "count": len(jon_all),
        "duplicates_within_list": len(jon_all) - len(set(jon_all)),
    }

    # ------------------------------------------------------------------
    # Step 2 (cross-check a): the old build's independently written
    # constants must contain the same sets.
    # ------------------------------------------------------------------
    old = parse_old_constants()
    for nb_name, old_name in OLD_BUILD_EQUALS.items():
        same = set(extracted[nb_name]) == set(old[old_name])
        report["checks"][f"old_build_{old_name}"] = "MATCH" if same else "MISMATCH"
        if not same:
            report["discrepancies"].append(
                f"{nb_name} vs old {old_name}: sets differ "
                f"(only-notebook: {sorted(set(extracted[nb_name]) - set(old[old_name]))}, "
                f"only-old: {sorted(set(old[old_name]) - set(extracted[nb_name]))})")
    mn9_old = [old["MN9_LEFT"], old["MN9_RIGHT"]]
    report["checks"]["old_build_MN9_pair"] = "MATCH" if mn9_old == list(mn9) else "MISMATCH"
    report["checks"]["old_build_DN1_1"] = (
        "MATCH" if old["DN1_1"] == extracted["id_DN1_1"][0] else "MISMATCH")
    report["checks"]["old_build_DN2_L"] = (
        "MATCH" if old["DN2_L"] == extracted["id_DN2_l"][0] else "MISMATCH")

    # ------------------------------------------------------------------
    # Step 3 (cross-check b): the v630 materialisation itself.
    # Every extracted ID must exist in the completeness file, and the
    # connectivity file's index columns must point at the same IDs the
    # completeness order assigns -- model.py relies on that silently.
    # ------------------------------------------------------------------
    df_comp = pd.read_csv(PATH_COMP, index_col=0)
    comp_ids = df_comp.index.to_numpy(dtype="int64")
    comp_set = set(comp_ids.tolist())
    report["checks"]["completeness_neurons"] = int(len(comp_set))

    every_id = set()
    for ids in extracted.values():
        every_id.update(ids)
    missing = sorted(every_id - comp_set)
    report["checks"]["extracted_ids_total"] = int(len(every_id))
    report["checks"]["extracted_ids_missing_from_v630"] = missing
    if missing:
        report["discrepancies"].append(
            f"{len(missing)} extracted ids are NOT in the v630 completeness set: {missing}")

    # Index <-> ID correspondence over the whole connectivity file, in
    # batches so the 87 MB parquet is never held whole in memory.
    pf = pq.ParquetFile(PATH_CON)
    bad_pre = bad_post = rows = 0
    for batch in pf.iter_batches(
            columns=["Presynaptic_ID", "Postsynaptic_ID",
                     "Presynaptic_Index", "Postsynaptic_Index"],
            batch_size=1_000_000):
        pre_id = batch.column("Presynaptic_ID").to_numpy()
        post_id = batch.column("Postsynaptic_ID").to_numpy()
        pre_ix = batch.column("Presynaptic_Index").to_numpy()
        post_ix = batch.column("Postsynaptic_Index").to_numpy()
        bad_pre += int((comp_ids[pre_ix] != pre_id).sum())
        bad_post += int((comp_ids[post_ix] != post_id).sum())
        rows += len(pre_id)
    report["checks"]["connectivity_rows_checked"] = int(rows)
    report["checks"]["index_id_mismatches_pre"] = bad_pre
    report["checks"]["index_id_mismatches_post"] = bad_post
    if bad_pre or bad_post:
        report["discrepancies"].append(
            f"connectivity index<->ID mapping broken: {bad_pre} pre, {bad_post} post mismatches")

    # Overlaps between populations: sensory sets should be disjoint, and a
    # surprise overlap is worth more than a silent one.
    pops = {PRETTY.get(k, k): v for k, v in extracted.items() if isinstance(v, list)}
    overlaps = {}
    names = sorted(pops)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            inter = set(pops[a]) & set(pops[b])
            if inter:
                overlaps[f"{a} & {b}"] = sorted(inter)
    report["checks"]["population_overlaps"] = overlaps

    # ------------------------------------------------------------------
    # Step 4: save the artefacts (one CSV per population + manifest).
    # ------------------------------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    artefact_files = {}
    for key, info in report["populations"].items():
        nb_name = info["notebook_name"].split(" ")[0]
        ids = extracted.get(nb_name) or info.get("ids")
        if ids is None:
            continue
        df = pd.DataFrame({"flywire_id": ids})
        df.to_csv(OUT / f"{key}.csv", index=False)
        artefact_files[key] = f"{key}.csv"

    manifest = {
        "artefact": "ConnectomeToBehaviour Part 2 neuron ID sets",
        "version": "v1",
        "extraction_date": "2026-11-23",
        "method": ("ID lists parsed as text from the upstream notebooks "
                   "(example.ipynb, figures.ipynb) of philshiu/Drosophila_brain_model; "
                   "cross-checked against the old build's constants.py (independent "
                   "transcription) and against the v630 materialisation files."),
        "upstream_repo": "https://github.com/philshiu/Drosophila_brain_model",
        "upstream_commit": "91bdd1e7dcf193f3e7ca5a8933497fcef63b7960",
        "model_py_sha256": sha256_of(UPSTREAM / "model.py"),
        "data_files": {
            "completeness": {"path": str(PATH_COMP), "sha256": sha256_of(PATH_COMP)},
            "connectivity": {"path": str(PATH_CON), "sha256": sha256_of(PATH_CON)},
        },
        "populations": {k: {"count": v["count"], "file": artefact_files.get(k)}
                        for k, v in report["populations"].items()},
        "checks": report["checks"],
        "discrepancies": report["discrepancies"],
        "not_extracted": ("SEZ neuron sets (types_and_ids) used by the Figure 2 "
                          "experiments: they exist only inside sez_neurons.pickle, a "
                          "binary executable artefact with no text source in the repo, "
                          "and were not loaded. See PART2-ID-SETS.md."),
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))

    print(json.dumps(report, indent=2))
    print(f"\nArtefacts written to {OUT}")


if __name__ == "__main__":
    main()
