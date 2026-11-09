"""
Automated data downloader and integrity verifier for ConnectomeToBehaviour.

Fetches the published adult Drosophila whole-brain connectome datasets:
1. v630 (Shiu et al., Nature 2024 baseline: completeness CSV, connectivity Parquet, and ground truth example run)
2. v783 (FlyWire final release / Eon Systems dataset)

Usage:
    python scripts/download_data.py [--target-dir DIR]
"""

import os
import sys
import argparse
import urllib.request
from pathlib import Path

# Public repository raw base URLs
GITHUB_SHIU_RAW = "https://raw.githubusercontent.com/philshiu/Drosophila_brain_model/main"
GITHUB_EON_RAW = "https://raw.githubusercontent.com/eonsystemspbc/fly-brain/main"

# Core files required for baseline simulation and validation
FILES_V630 = {
    "2023_03_23_completeness_630_final.csv": {
        "url": f"{GITHUB_SHIU_RAW}/2023_03_23_completeness_630_final.csv",
        "approx_size_mb": 3.0,
        "description": "Neuron metadata & cell IDs for FlyWire v630 materialization",
    },
    "2023_03_23_connectivity_630_final.parquet": {
        "url": f"{GITHUB_SHIU_RAW}/2023_03_23_connectivity_630_final.parquet",
        "approx_size_mb": 86.6,
        "description": "Synaptic connectivity matrix for FlyWire v630 materialization",
    },
    "results/example/sugarR.parquet": {
        "url": f"{GITHUB_SHIU_RAW}/results/example/sugarR.parquet",
        "approx_size_mb": 2.2,
        "description": "Published Shiu et al. (2024) 30-trial sugar simulation ground truth",
    },
}

FILES_V783 = {
    "Completeness_783.csv": {
        "url": f"{GITHUB_SHIU_RAW}/Completeness_783.csv",
        "approx_size_mb": 3.3,
        "description": "Neuron completeness metadata for FlyWire v783 release",
    },
    "Connectivity_783.parquet": {
        "url": f"{GITHUB_SHIU_RAW}/Connectivity_783.parquet",
        "approx_size_mb": 100.8,
        "description": "Full synaptic connectivity matrix for FlyWire v783 release",
    },
}


def download_file(url: str, dest_path: Path):
    """Download a file with console progress indicator."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = dest_path.with_suffix(".tmp")

    def reporthook(count, block_size, total_size):
        if total_size > 0:
            percent = int(count * block_size * 100 / total_size)
            downloaded_mb = (count * block_size) / (1024 * 1024)
            total_mb = total_size / (1024 * 1024)
            sys.stdout.write(f"\r  -> Downloading: {percent}% ({downloaded_mb:.1f}/{total_mb:.1f} MB)")
            sys.stdout.flush()

    try:
        urllib.request.urlretrieve(url, temp_path, reporthook=reporthook)
        if temp_path.exists():
            if dest_path.exists():
                dest_path.unlink()
            temp_path.rename(dest_path)
        sys.stdout.write("\n")
    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise RuntimeError(f"Failed to download {url}: {e}")


def verify_or_download(target_dir: Path, include_v783: bool = False):
    print("=" * 65)
    print(" ConnectomeToBehaviour — Dataset Download & Integrity Check")
    print("=" * 65)
    print(f"Target data directory: {target_dir.resolve()}\n")

    files_to_check = dict(FILES_V630)
    if include_v783:
        files_to_check.update(FILES_V783)

    for rel_path, info in files_to_check.items():
        dest = target_dir / rel_path
        print(f"Checking: {rel_path}")
        print(f"  Description: {info['description']}")

        if dest.exists() and dest.stat().st_size > 1024:
            size_mb = dest.stat().st_size / (1024 * 1024)
            print(f"  [OK] Already present ({size_mb:.1f} MB)\n")
        else:
            print(f"  [DOWNLOAD NEEDED] (~{info['approx_size_mb']:.1f} MB)")
            download_file(info["url"], dest)
            print(f"  [OK] Saved to {dest.resolve()}\n")

    print("=" * 65)
    print(" All requested connectome datasets verified successfully.")
    print("=" * 65)


def main():
    project_root = Path(__file__).resolve().parent.parent
    default_dir = project_root / "Drosophila_brain_model-main"

    parser = argparse.ArgumentParser(description="Download connectome datasets for ConnectomeToBehaviour.")
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=default_dir,
        help="Destination directory for connectome files (default: Drosophila_brain_model-main/)",
    )
    parser.add_argument(
        "--include-v783",
        action="store_true",
        help="Also download the v783 dataset files (~104 MB)",
    )

    args = parser.parse_args()
    verify_or_download(args.target_dir, include_v783=args.include_v783)


if __name__ == "__main__":
    main()
