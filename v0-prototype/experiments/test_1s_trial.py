import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import time
import numpy as np
import pandas as pd
from brian2 import ms, second, Hz, volt, mV, prefs, SpikeMonitor, Network
prefs.codegen.target = "numpy"

from src.brain import FlyBrain, SUGAR_GRNS_RIGHT, MN9_LEFT, MN9_RIGHT

brain = FlyBrain()
brain.activate(SUGAR_GRNS_RIGHT, freq_hz=150.0)

# Build network once
t0 = time.time()
net, spk_mon = brain._build_network(duration_ms=1000.0)
print(f"Network built in {time.time() - t0:.2f}s")

# Run 1 trial of 1.0s
t0 = time.time()
net.run(1.0 * second)
t_run = time.time() - t0
spikes = len(spk_mon.i)
print(f"1.0s trial completed in {t_run:.2f}s with {spikes} spikes")

mn9_l = len([idx for idx in spk_mon.i if brain.i2flyid[idx] == MN9_LEFT])
mn9_r = len([idx for idx in spk_mon.i if brain.i2flyid[idx] == MN9_RIGHT])
print(f"MN9 Left: {mn9_l} spikes ({mn9_l / 1.0} Hz)")
print(f"MN9 Right: {mn9_r} spikes ({mn9_r / 1.0} Hz)")
