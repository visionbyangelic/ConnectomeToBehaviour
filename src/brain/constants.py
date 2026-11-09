"""
Biophysical constants, equations, and known functional neuron sets for the Drosophila brain LIF model.

References:
- Shiu et al. (Nature 2024): A Drosophila computational brain model reveals how neural circuits generate behavior.
- Kakaria and de Bivort (2017): Biophysical parameters (resting potential -52 mV, threshold -45 mV, membrane timescale 20 ms).
- Jürgensen et al. (2021): Synaptic alpha time constant (tau = 5 ms).
- Lazar et al. (2020): Refractory period (2.2 ms).
- Paul et al. (2015): Post-synaptic conduction delay (1.8 ms).
- Eckstein et al. (2024): Neurotransmitter classification determining excitation vs. inhibition.
"""

from textwrap import dedent

# Default biophysical parameters
DEFAULT_PARAMS = {
    # Simulation timing
    't_run': 1000.0,              # ms: duration of a single trial
    'n_run': 1,                   # number of trials
    'dt': 0.1,                    # ms: integration timestep

    # Electrophysiological properties (Kakaria and de Bivort 2017)
    'v_0': -52.0,                 # mV: resting potential
    'v_rst': -52.0,               # mV: reset potential after action potential
    'v_th': -45.0,                # mV: threshold for action potential generation
    't_mbr': 20.0,                # ms: membrane time scale (C_m * R_m)

    # Synaptic dynamics (Jürgensen et al.)
    'tau': 5.0,                   # ms: alpha-synapse time constant

    # Refractory period (Lazar et al. 2020)
    't_rfc': 2.2,                 # ms: absolute refractory period

    # Conduction & synaptic delay (Paul et al. 2015)
    't_dly': 1.8,                 # ms: axonal + synaptic delay

    # Synaptic weight scale (Shiu et al. 2024)
    'w_syn': 0.275,               # mV: baseline PSP amplitude per anatomical synapse
    'r_poi': 150.0,               # Hz: default Poisson stimulation frequency
    'r_poi2': 0.0,                # Hz: default secondary Poisson stimulation frequency
    'f_poi': 250.0,               # scaling factor for Poisson external sensory input

    # Differential equations for Leaky Integrate-and-Fire neurons with alpha-conductance
    'eqs': dedent('''
        dv/dt = (v_0 - v + g) / t_mbr : volt (unless refractory)
        dg/dt = -g / tau               : volt (unless refractory)
        rfc                            : second
    '''),
    'eq_th': 'v > v_th',
    'eq_rst': 'v = v_rst; g = 0 * mV',
}

# ==============================================================================
# Known Functional Cell Types (FlyWire v630 IDs from Shiu et al. 2024)
# ==============================================================================

# Labellar sugar-sensing gustatory receptor neurons (Right hemisphere, 21 neurons)
SUGAR_GRNS_RIGHT = [
    720575940624963786, 720575940630233916, 720575940637568838, 720575940638202345, 720575940617000768,
    720575940630797113, 720575940632889389, 720575940621754367, 720575940621502051, 720575940640649691,
    720575940639332736, 720575940616885538, 720575940639198653, 720575940620900446, 720575940617937543,
    720575940632425919, 720575940633143833, 720575940612670570, 720575940628853239, 720575940629176663,
    720575940611875570,
]

# Labellar sugar-sensing gustatory receptor neurons (Left hemisphere, 10 neurons)
SUGAR_GRNS_LEFT = [
    720575940620589838, 720575940631147148, 720575940608305161, 720575940629388135, 720575940630968335,
    720575940606801282, 720575940617398502, 720575940616167218, 720575940620296641, 720575940627961104,
]

# Labellar bitter-sensing gustatory receptor neurons (21 neurons)
BITTER_GRNS = [
    720575940621778381, 720575940602353632, 720575940617094208, 720575940619197093, 720575940626287336,
    720575940618600651, 720575940627692048, 720575940630195909, 720575940646212996, 720575940610483162,
    720575940645743412, 720575940627578156, 720575940622298631, 720575940621008895, 720575940629146711,
    720575940610259370, 720575940610481370, 720575940619028208, 720575940614281266, 720575940613061118,
    720575940604027168,
]

# Labellar water-sensing gustatory receptor neurons (18 neurons)
WATER_GRNS = [
    720575940612950568, 720575940631898285, 720575940606002609, 720575940612579053, 720575940622902535,
    720575940616177458, 720575940660292225, 720575940622486922, 720575940613786774, 720575940629852866,
    720575940625861168, 720575940613996959, 720575940617857694, 720575940644965399, 720575940625203504,
    720575940630553415, 720575940635172191, 720575940634796536,
]

# Proboscis extension motor neuron 9 (MN9)
MN9_LEFT = 720575940660219265
MN9_RIGHT = 720575940645521262
MN9_NEURONS = [MN9_LEFT, MN9_RIGHT]

# Antennal mechanosensory / Johnston's Organ Neurons (JON) Descending Command Targets
DN1_1 = 720575940616185531
DN2_L = 720575940629806974
