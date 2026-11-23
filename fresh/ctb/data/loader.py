"""Loading the FlyWire v630 connectome -- with the hashes checked first.

The model stands or falls on two files: the completeness CSV (which neurons
exist, and in which order) and the connectivity parquet (which of them are
connected, with how many synapses, and with what sign). Part 1 downloaded
them and recorded their SHA-256 hashes; this loader re-computes the hashes
on every load and refuses to build anything from files that do not match.
A silent file swap upstream would otherwise change the connectome under
the model without anyone noticing.

Conventions established here, used everywhere downstream:

- Brian index *i* is row *i* of the completeness CSV -- the same order the
  upstream model uses, and the order the connectivity file's index columns
  refer to. Part 2 verified that correspondence over all 14,687,178 edges
  (0 mismatches); `check_index_consistency` below repeats the check.
- Populations are never typed into code by hand. They are loaded from the
  versioned Part 2 artefacts (``id_sets_v1``), whose manifest records where
  every ID came from and what it was cross-checked against.
"""

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

COMPLETENESS_NAME = "2023_03_23_completeness_630_final.csv"
CONNECTIVITY_NAME = "2023_03_23_connectivity_630_final.parquet"

# SHA-256 of the two files as downloaded and content-verified in Part 1
# (record: fresh/PART1-DATA.md). If upstream ever serves different bytes,
# loading stops here rather than simulating a different brain.
EXPECTED_SHA256 = {
    COMPLETENESS_NAME:
        "e6b71e17671a9bdb05f55e4bc6774640a1418cb7a05125e0fc994ad40f9bfdfb",
    CONNECTIVITY_NAME:
        "94db8c650533bc36ffa3223f2e62325d5648b8d6bd31c3a4e1c804628c7557b3",
}


class DataHashMismatch(RuntimeError):
    """A data file's SHA-256 does not match the Part 1 record."""


def sha256_of(path):
    """SHA-256 of a file, read in chunks (the parquet is ~87 MB)."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_data_files(data_dir):
    """Check both data files against the Part 1 hashes.

    Returns {filename: actual_sha256}. Raises FileNotFoundError for a
    missing file and DataHashMismatch for a changed one -- loudly, before
    any simulation is built on top of them.
    """
    data_dir = Path(data_dir)
    actual = {}
    for name, expected in EXPECTED_SHA256.items():
        path = data_dir / name
        if not path.exists():
            raise FileNotFoundError(f"data file missing: {path}")
        actual[name] = sha256_of(path)
        if actual[name] != expected:
            raise DataHashMismatch(
                f"{name}: SHA-256 {actual[name]} does not match the "
                f"Part 1 record {expected}. Refusing to load.")
    return actual


class ConnectomeData:
    """The v630 connectome in memory.

    ids    -- FlyWire IDs in completeness-CSV row order; ids[i] is the
              FlyWire ID of Brian neuron i.
    edges  -- the connectivity table (one row per directed edge) with
              columns Presynaptic_ID / Postsynaptic_ID (FlyWire IDs),
              Presynaptic_Index / Postsynaptic_Index (Brian indices),
              Connectivity (anatomical synapse count) and Excitatory
              (+1/-1, the predicted-transmitter sign).
    """

    def __init__(self, ids, edges, file_hashes=None, source="files"):
        self.ids = np.asarray(ids, dtype=np.int64)
        self.edges = edges
        self.file_hashes = file_hashes or {}
        self.source = source
        # FlyWire ID -> Brian index. A dict is the honest structure here:
        # the IDs are large, sparse integers, not a range.
        self._index_of = {int(fid): i for i, fid in enumerate(self.ids)}

    def __len__(self):
        return len(self.ids)

    def index_of(self, flywire_ids):
        """Brian indices for FlyWire IDs. A missing ID is a KeyError with
        the offending ID named -- upstream let a bare KeyError escape from
        deep inside a parallel run; we fail at the boundary instead."""
        out = []
        for fid in flywire_ids:
            fid = int(fid)
            if fid not in self._index_of:
                raise KeyError(f"FlyWire ID {fid} is not in the v630 "
                               f"completeness set")
            out.append(self._index_of[fid])
        return np.asarray(out, dtype=np.int64)


def load_connectome(data_dir, verify=True):
    """Load both v630 files from `data_dir` into a ConnectomeData.

    With verify=True (the default, and the only mode the runner uses) the
    SHA-256 of each file is checked against the Part 1 record first.
    """
    data_dir = Path(data_dir)
    hashes = verify_data_files(data_dir) if verify else {}
    # index_col=0: the CSV's first column is the FlyWire ID and becomes the
    # index, so the row order -- hence the Brian index order -- is the
    # file's own order, exactly as upstream takes it.
    df_comp = pd.read_csv(data_dir / COMPLETENESS_NAME, index_col=0)
    edges = pd.read_parquet(data_dir / CONNECTIVITY_NAME)
    # Slim the index/count columns; 14.7M rows of int64 add up.
    for col in ("Presynaptic_Index", "Postsynaptic_Index", "Connectivity"):
        edges[col] = edges[col].astype(np.int32)
    edges["Excitatory"] = edges["Excitatory"].astype(np.int8)
    return ConnectomeData(df_comp.index.to_numpy(dtype=np.int64), edges,
                          file_hashes=hashes, source=str(data_dir))


def check_index_consistency(data):
    """Count rows where the connectivity file's index columns disagree
    with its ID columns, given the completeness order.

    The upstream model trusts this correspondence silently; Part 2 checked
    it over every edge and found 0 mismatches. Returns the mismatch count
    (0 is the only acceptable answer for the hashed files).
    """
    pre_bad = (data.ids[data.edges["Presynaptic_Index"].to_numpy()]
               != data.edges["Presynaptic_ID"].to_numpy())
    post_bad = (data.ids[data.edges["Postsynaptic_Index"].to_numpy()]
                != data.edges["Postsynaptic_ID"].to_numpy())
    return int(pre_bad.sum() + post_bad.sum())


def load_populations(id_sets_dir, data):
    """Load the Part 2 ID-set artefacts as named populations of Brian
    indices: {population_name: np.ndarray of Brian indices}.

    Counts are validated against the artefacts' own manifest.json, so a
    truncated or edited CSV fails here rather than quietly shrinking a
    stimulus. The FlyWire IDs themselves are read from the CSVs -- they
    are never re-typed into code (Part 2 obligation).
    """
    id_sets_dir = Path(id_sets_dir)
    manifest = json.loads((id_sets_dir / "manifest.json").read_text())
    populations = {}
    for name, info in manifest["populations"].items():
        ids = pd.read_csv(id_sets_dir / info["file"])["flywire_id"]
        if len(ids) != info["count"]:
            raise ValueError(
                f"population {name}: {len(ids)} IDs in {info['file']}, "
                f"manifest says {info['count']}")
        populations[name] = data.index_of(ids.to_numpy())
    return populations
