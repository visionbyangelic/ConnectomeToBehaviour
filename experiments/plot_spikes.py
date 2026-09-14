"""
Plot raster plot and population firing rate from simulation parquet file.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

repo_dir = Path(__file__).resolve().parent.parent / 'Drosophila_brain_model-main'
parquet_path = repo_dir / 'results' / 'test' / 'test_sugar_100ms.parquet'

if not parquet_path.exists():
    print(f"File not found: {parquet_path}")
    sys.exit(1)

df = pd.read_parquet(parquet_path)
df['t_ms'] = df['t'] * 1000.0

neu_sugar = set([
    720575940624963786, 720575940630233916, 720575940637568838,
    720575940638202345, 720575940617000768, 720575940630797113,
    720575940632889389, 720575940621754367, 720575940621502051,
    720575940640649691, 720575940639332736, 720575940616885538,
    720575940639198653, 720575940620900446, 720575940617937543,
    720575940632425919, 720575940633143833, 720575940612670570,
    720575940628853239, 720575940629176663, 720575940611875570
])

unique_neurons = df['flywire_id'].unique().tolist()
sensory_in_data = [n for n in unique_neurons if n in neu_sugar]
downstream = [n for n in unique_neurons if n not in neu_sugar]

ordered_neurons = sensory_in_data + downstream
neuron_to_idx = {nid: i for i, nid in enumerate(ordered_neurons)}
df['neuron_idx'] = df['flywire_id'].map(neuron_to_idx)
df['is_sensory'] = df['flywire_id'].isin(neu_sugar)

plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
fig.patch.set_facecolor('#0f172a')
ax1.set_facecolor('#1e293b')
ax2.set_facecolor('#1e293b')

sensory_df = df[df['is_sensory']]
downstream_df = df[~df['is_sensory']]

ax1.scatter(downstream_df['t_ms'], downstream_df['neuron_idx'], s=6, c='#38bdf8', alpha=0.75, label=f'Downstream Neurons ({len(downstream)} active)')
ax1.scatter(sensory_df['t_ms'], sensory_df['neuron_idx'], s=14, c='#f59e0b', alpha=0.9, label=f'Sugar Sensory Neurons ({len(sensory_in_data)} driven at 150 Hz)')

ax1.set_ylabel('Active Neuron Index', fontsize=12, fontweight='bold', color='#e2e8f0')
ax1.set_title('Live Fruit Fly Connectome Activity — 100 ms Biological Time (Shiu et al. LIF Model)', fontsize=13, fontweight='bold', color='#f8fafc', pad=12)
ax1.legend(loc='upper right', framealpha=0.85, facecolor='#0f172a', edgecolor='#334155', fontsize=10)
ax1.grid(True, linestyle='--', alpha=0.2, color='#94a3b8')

bins = np.linspace(0, 100, 51)
ax2.hist([downstream_df['t_ms'], sensory_df['t_ms']], bins=bins, stacked=True, color=['#38bdf8', '#f59e0b'], label=['Downstream', 'Sensory'])
ax2.set_xlabel('Biological Time (milliseconds)', fontsize=12, fontweight='bold', color='#e2e8f0')
ax2.set_ylabel('Spike Count / 2ms', fontsize=11, fontweight='bold', color='#e2e8f0')
ax2.grid(True, linestyle='--', alpha=0.2, color='#94a3b8')

plt.xlim(0, 100)
plt.tight_layout()

out_png = repo_dir / 'results' / 'test' / 'spike_raster_100ms.png'
plt.savefig(out_png, dpi=200, facecolor=fig.get_facecolor(), bbox_inches='tight')
print(f"Graph saved to: {out_png}")
