import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Check CSV files
for name, p in [
    ("v630 completeness", ROOT / "Drosophila_brain_model-main" / "2023_03_23_completeness_630_final.csv"),
    ("v783 completeness", ROOT / "Drosophila_brain_model-main" / "Completeness_783.csv"),
]:
    if p.exists():
        df = pd.read_csv(p, nrows=10)
        print(f"=== {name} ===")
        print("Columns:", list(df.columns))
        print("First 2 rows:")
        print(df.head(2))

# Check sez_neurons.pickle
import pickle
sez_path = ROOT / "Drosophila_brain_model-main" / "sez_neurons.pickle"
if sez_path.exists():
    with open(sez_path, "rb") as f:
        sez = pickle.load(f)
    print("\n=== sez_neurons.pickle keys ===")
    print(list(sez.keys()) if isinstance(sez, dict) else type(sez))
    if isinstance(sez, dict):
        for k, v in list(sez.items())[:10]:
            print(f"sez['{k}']: type={type(v)}, len={len(v) if hasattr(v, '__len__') else v}")

