"""Q0 — pinned artefact verification (PART4-SENSORY-SPECS §7.1).

The artefact under qualification is the FlyBody model shipping inside the
installed FlyGym 2.1.1, not any other flybody build. Before anything runs,
re-hash the five model files and compare against the values §7.1 pinned when
the specs were written. A mismatch stops the gate before it starts: there is
no sense qualifying a body that is not the body the specs froze.

Also recorded here, because §7.1 asks for them in the same breath: the mesh
cache state (the gate must be able to say no download happened during it) and
the environment versions the gate ran under.
"""

import hashlib
import importlib.metadata
import json
import time
from pathlib import Path

import flygym
from flygym.utils.assets_lazy_loading import get_cache_root

# The five pinned files and their §7.1 SHA-256 values, copied from the specs.
PINNED = {
    "fruitfly.xml": "66e495951d1713559066e18eae55e9ed0e368350dd9006bea0be2b615bfb1a2c",
    "joints.yaml": "b90bf60cc04fc3b32350d58e00d6f2f18c202073a54644a8b3c514c2431f977a",
    "actuators.yaml": "31feee850de6046860f8ef486471fab9b762a733857845986b019853277fd317",
    "mujoco_globals.yaml": "7ea81498d8cf02ce6380a4f9d9a4b3610b8acbedfa81f19844ad8c2c4901e350",
    "rigging.yaml": "eb852760f6cc7fedea4e2d75cff89b0b4eec6dad09b67368266644d8db628737",
}

# Upstream's own word for its FlyBody support, from the FlyBody class docstring
# in flygym/compose/fly/flybody.py. §7.1 wants it quoted in the gate record.
EXPERIMENTAL_LABEL = "Support for the FlyBody body model is experimental."


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    t0 = time.time()
    model_dir = Path(flygym.__file__).parent / "assets" / "model" / "flybody"

    files = {}
    all_match = True
    for name, pinned in PINNED.items():
        measured = sha256_of(model_dir / name)
        match = measured == pinned
        all_match &= match
        files[name] = {"pinned": pinned, "measured": measured, "match": match}

    # Mesh cache: FlyBody meshes are an S3 lazy-download, cached at Part 1b.
    # Snapshot what is cached now; the gate record compares against this to
    # show the gate itself downloaded nothing.
    cache_root = get_cache_root()
    mesh_dir = cache_root / "flybody_fullsize_meshes_20260623a"
    cache_state = {
        "cache_root": str(cache_root),
        "flybody_mesh_dir": str(mesh_dir),
        "flybody_mesh_dir_present": mesh_dir.is_dir(),
        "cached_dirs": sorted(p.name for p in cache_root.iterdir())
        if cache_root.is_dir()
        else [],
    }

    result = {
        "step": "Q0",
        "model_dir": str(model_dir),
        "files": files,
        "all_match": all_match,
        "mesh_cache": cache_state,
        "experimental_label": EXPERIMENTAL_LABEL,
        "versions": {
            "flygym": importlib.metadata.version("flygym"),
            "mujoco": importlib.metadata.version("mujoco"),
            "numpy": importlib.metadata.version("numpy"),
        },
        "verdict": "PASS" if all_match else "FAIL",
        "wall_clock_s": time.time() - t0,
    }

    out = Path(__file__).resolve().parents[2] / "results" / "body_qualification" / "q0.json"
    out.write_text(json.dumps(result, indent=2))
    print(f"Q0 verdict: {result['verdict']} "
          f"({sum(f['match'] for f in files.values())}/5 hashes match, "
          f"{result['wall_clock_s']:.1f} s)")
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
