"""
Quick test simulation of the adult Drosophila connectome using Shiu et al. (2024) LIF model.
"""

import os
import sys
from pathlib import Path
from brian2 import ms, Hz

# Add Drosophila_brain_model-main to path for model imports
repo_dir = Path(__file__).resolve().parent.parent / 'Drosophila_brain_model-main'
sys.path.append(str(repo_dir))

from model import run_exp, default_params
import utils as utl

if __name__ == '__main__':
    print("=== Starting Quick Connectome Simulation Test ===")
    
    # Ensure output directory exists
    out_dir = repo_dir / 'results' / 'test'
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure fast test parameters
    test_params = default_params.copy()
    test_params['t_run'] = 100 * ms  # 100 ms of biological time
    test_params['n_run'] = 1         # 1 single trial
    
    # 21 Sugar-sensing gustatory sensory neurons
    neu_sugar = [
        720575940624963786, 720575940630233916, 720575940637568838,
        720575940638202345, 720575940617000768, 720575940630797113,
        720575940632889389, 720575940621754367, 720575940621502051,
        720575940640649691, 720575940639332736, 720575940616885538,
        720575940639198653, 720575940620900446, 720575940617937543,
        720575940632425919, 720575940633143833, 720575940612670570,
        720575940628853239, 720575940629176663, 720575940611875570,
    ]
    
    comp_file = repo_dir / '2023_03_23_completeness_630_final.csv'
    con_file = repo_dir / '2023_03_23_connectivity_630_final.parquet'
    
    print("Loading connectome (v630: ~125k neurons) and running 1 trial (100 ms)...")
    run_exp(
        exp_name='test_sugar_100ms',
        neu_exc=neu_sugar,
        path_res=str(out_dir),
        path_comp=str(comp_file),
        path_con=str(con_file),
        params=test_params,
        n_proc=1,
        force_overwrite=True
    )
    
    output_file = out_dir / 'test_sugar_100ms.parquet'
    if output_file.exists():
        df = utl.load_exps([str(output_file)])
        print("\n=== SUCCESS! Simulation Complete ===")
        print(f"Output saved to: {output_file}")
        print(f"Total spikes generated in 100 ms: {len(df)}")
        print(f"Unique active neurons: {df['flywire_id'].nunique()}")
    else:
        print("\n=== Error: Output file was not generated ===")
