"""
FlyBrain: High-level Python API for whole-brain Drosophila connectome Leaky Integrate-and-Fire simulation.

Implements the connectome-constrained alpha-synapse LIF model from Shiu et al. (Nature 2024),
providing an intuitive interface for sensory activation, neuron silencing (lesions),
multi-trial simulation, and spike/rate analysis.
"""

from pathlib import Path
from typing import List, Dict, Optional, Set, Union
import numpy as np
import pandas as pd
from brian2 import NeuronGroup, Synapses, PoissonInput, SpikeMonitor, Network, prefs
from brian2 import mV, ms, Hz, volt, second

# Set Brian2 code generation target to numpy (avoids Cython compilation overhead/warnings)
prefs.codegen.target = "numpy"

from .constants import (
    DEFAULT_PARAMS,
    SUGAR_GRNS_RIGHT,
    BITTER_GRNS,
    WATER_GRNS,
    MN9_LEFT,
    MN9_RIGHT,
    MN9_NEURONS,
)


class FlyBrain:
    """
    Whole-brain Leaky Integrate-and-Fire (LIF) neural network model of Drosophila melanogaster.
    """

    def __init__(
        self,
        path_completeness: Optional[Union[str, Path]] = None,
        path_connectivity: Optional[Union[str, Path]] = None,
        custom_params: Optional[Dict] = None,
        preload_connectome: bool = True,
    ):
        """
        Initialize the FlyBrain connectome model.

        Parameters
        ----------
        path_completeness : Path or str, optional
            Path to the neuron completeness CSV table (FlyWire materialization).
        path_connectivity : Path or str, optional
            Path to the synaptic connectivity Parquet file.
        custom_params : dict, optional
            Biophysical overrides to DEFAULT_PARAMS.
        preload_connectome : bool, default=True
            Whether to read and index the neuron metadata immediately upon instantiation.
        """
        project_root = Path(__file__).resolve().parent.parent.parent

        # Default paths to the verified local v630 dataset in Drosophila_brain_model-main
        default_comp = project_root / "Drosophila_brain_model-main" / "2023_03_23_completeness_630_final.csv"
        default_con = project_root / "Drosophila_brain_model-main" / "2023_03_23_connectivity_630_final.parquet"

        self.path_comp = Path(path_completeness) if path_completeness else default_comp
        self.path_con = Path(path_connectivity) if path_connectivity else default_con

        if not self.path_comp.exists():
            raise FileNotFoundError(f"Completeness file not found at: {self.path_comp}")
        if not self.path_con.exists():
            raise FileNotFoundError(f"Connectivity file not found at: {self.path_con}")

        # Biophysical parameters
        self.params = dict(DEFAULT_PARAMS)
        if custom_params:
            self.params.update(custom_params)

        # Active stimuli and lesions
        self._primary_stimuli: List[int] = []
        self._primary_freq_hz: float = 150.0
        self._secondary_stimuli: List[int] = []
        self._secondary_freq_hz: float = 0.0
        self._silenced_neurons: List[int] = []

        # Connectome index tables
        self.df_comp: Optional[pd.DataFrame] = None
        self.flyid2i: Dict[int, int] = {}
        self.i2flyid: Dict[int, int] = {}
        self.total_neurons: int = 0

        # Simulation output caching
        self.last_spike_df: Optional[pd.DataFrame] = None
        self.last_rates_series: Optional[pd.Series] = None

        if preload_connectome:
            self._load_neuron_metadata()

    def _load_neuron_metadata(self):
        """Load and index neuron completeness table."""
        if self.df_comp is None:
            self.df_comp = pd.read_csv(self.path_comp, index_col=0)
            self.flyid2i = {fly_id: idx for idx, fly_id in enumerate(self.df_comp.index)}
            self.i2flyid = {idx: fly_id for fly_id, idx in self.flyid2i.items()}
            self.total_neurons = len(self.df_comp)

    def activate(self, neuron_ids: List[int], freq_hz: float = 150.0) -> "FlyBrain":
        """
        Set primary external Poisson excitation on a set of neurons.

        Parameters
        ----------
        neuron_ids : list of int
            FlyWire IDs of sensory/input neurons to activate.
        freq_hz : float, default=150.0
            Stimulation frequency in Hz.
        """
        self._primary_stimuli = list(neuron_ids)
        self._primary_freq_hz = float(freq_hz)
        return self

    def activate_secondary(self, neuron_ids: List[int], freq_hz: float = 150.0) -> "FlyBrain":
        """
        Set secondary external Poisson excitation for dual-modality experiments
        (e.g., simultaneous sugar + bitter stimulation).

        Parameters
        ----------
        neuron_ids : list of int
            FlyWire IDs of secondary input neurons.
        freq_hz : float, default=150.0
            Stimulation frequency in Hz.
        """
        self._secondary_stimuli = list(neuron_ids)
        self._secondary_freq_hz = float(freq_hz)
        return self

    def silence(self, neuron_ids: List[int]) -> "FlyBrain":
        """
        In silico lesion/silencing of specified neurons by zeroing all their outgoing synaptic weights.

        Parameters
        ----------
        neuron_ids : list of int
            FlyWire IDs of neurons to silence.
        """
        self._silenced_neurons = list(neuron_ids)
        return self

    def reset_stimuli(self) -> "FlyBrain":
        """Clear all active stimuli and silencing configurations."""
        self._primary_stimuli = []
        self._primary_freq_hz = 150.0
        self._secondary_stimuli = []
        self._secondary_freq_hz = 0.0
        self._silenced_neurons = []
        return self

    def _build_network(self, duration_ms: float):
        """Construct the Brian2 Network instance with LIF equations and alpha-synapses."""
        self._load_neuron_metadata()

        df_con = pd.read_parquet(self.path_con)

        brian_params = {
            'v_0': self.params['v_0'] * mV,
            'v_rst': self.params['v_rst'] * mV,
            'v_th': self.params['v_th'] * mV,
            't_mbr': self.params['t_mbr'] * ms,
            'tau': self.params['tau'] * ms,
            't_rfc': self.params['t_rfc'] * ms,
            't_dly': self.params['t_dly'] * ms,
            'w_syn': self.params['w_syn'] * mV,
            'r_poi': self._primary_freq_hz * Hz,
            'r_poi2': self._secondary_freq_hz * Hz,
            'f_poi': self.params['f_poi'],
            'eqs': self.params['eqs'],
            'eq_th': self.params['eq_th'],
            'eq_rst': self.params['eq_rst'],
        }

        # Create NeuronGroup
        neu = NeuronGroup(
            N=self.total_neurons,
            model=brian_params['eqs'],
            method='linear',
            threshold=brian_params['eq_th'],
            reset=brian_params['eq_rst'],
            refractory='rfc',
            name='drosophila_neurons',
            namespace=brian_params,
        )
        neu.v = brian_params['v_0']
        neu.g = 0 * volt
        neu.rfc = brian_params['t_rfc']

        # Create Synapses
        syn = Synapses(
            neu, neu,
            'w : volt',
            on_pre='g += w',
            delay=brian_params['t_dly'],
            name='drosophila_synapses',
        )
        i_pre = df_con['Presynaptic_Index'].values
        i_post = df_con['Postsynaptic_Index'].values
        syn.connect(i=i_pre, j=i_post)

        # Scale weights by sign and synapse count
        syn.w = df_con['Excitatory x Connectivity'].values * brian_params['w_syn']

        # Apply in silico lesion/silencing if specified
        if self._silenced_neurons:
            for slnc_id in self._silenced_neurons:
                if slnc_id in self.flyid2i:
                    idx = self.flyid2i[slnc_id]
                    syn.w[f'{idx} == i'] = 0 * mV

        # Add external Poisson sensory inputs
        poisson_inputs = []
        if self._primary_stimuli and self._primary_freq_hz > 0:
            for stim_id in self._primary_stimuli:
                if stim_id in self.flyid2i:
                    idx = self.flyid2i[stim_id]
                    poi = PoissonInput(
                        target=neu[idx],
                        target_var='v',
                        N=1,
                        rate=brian_params['r_poi'],
                        weight=brian_params['w_syn'] * brian_params['f_poi'],
                    )
                    neu[idx].rfc = 0 * ms
                    poisson_inputs.append(poi)

        if self._secondary_stimuli and self._secondary_freq_hz > 0:
            for stim_id in self._secondary_stimuli:
                if stim_id in self.flyid2i:
                    idx = self.flyid2i[stim_id]
                    poi = PoissonInput(
                        target=neu[idx],
                        target_var='v',
                        N=1,
                        rate=brian_params['r_poi2'],
                        weight=brian_params['w_syn'] * brian_params['f_poi'],
                    )
                    neu[idx].rfc = 0 * ms
                    poisson_inputs.append(poi)

        # Spike Monitor
        spk_mon = SpikeMonitor(neu)
        net = Network(neu, syn, spk_mon, *poisson_inputs)

        return net, spk_mon

    def simulate(
        self,
        duration_ms: float = 100.0,
        n_trials: int = 1,
        exp_name: str = "simulation",
        verbose: bool = True,
    ) -> pd.DataFrame:
        """
        Execute the whole-brain LIF simulation.

        Parameters
        ----------
        duration_ms : float, default=100.0
            Biological duration of each trial in milliseconds.
        n_trials : int, default=1
            Number of stochastic Poisson trials to execute.
        exp_name : str, default='simulation'
            Tag name for the experiment.
        verbose : bool, default=True
            Whether to print progress messages.

        Returns
        -------
        df_spikes : pd.DataFrame
            DataFrame containing all recorded spikes: ['t', 'trial', 'flywire_id', 'exp_name'].
        """
        self._load_neuron_metadata()

        all_ts = []
        all_trials = []
        all_ids = []

        for trial_idx in range(n_trials):
            if verbose:
                print(f"[FlyBrain] Running trial {trial_idx + 1}/{n_trials} ({duration_ms} ms)...")

            net, spk_mon = self._build_network(duration_ms)
            net.run(duration=duration_ms * ms)

            spike_trains = spk_mon.spike_trains()
            for brian_idx, times in spike_trains.items():
                if len(times) > 0:
                    fly_id = self.i2flyid[brian_idx]
                    for t in times:
                        all_ts.append(float(t / second))
                        all_trials.append(trial_idx)
                        all_ids.append(fly_id)

        df = pd.DataFrame({
            't': all_ts,
            'trial': all_trials,
            'flywire_id': all_ids,
            'exp_name': exp_name,
        })

        self.last_spike_df = df

        # Compute per-neuron average firing rate across total simulated time
        total_time_s = (duration_ms / 1000.0) * n_trials
        if total_time_s > 0 and len(df) > 0:
            counts = df.groupby('flywire_id').size()
            self.last_rates_series = counts / total_time_s
        else:
            self.last_rates_series = pd.Series(dtype=float)

        if verbose:
            n_active = len(self.last_rates_series)
            n_spikes = len(df)
            print(f"[FlyBrain] Done: {n_spikes} total spikes across {n_active} active neurons.")

        return df

    def get_spike_dataframe(self) -> pd.DataFrame:
        """Return DataFrame of spikes from the most recent simulation."""
        if self.last_spike_df is None:
            raise RuntimeError("No simulation has been run yet. Call simulate() first.")
        return self.last_spike_df

    def get_firing_rates(self) -> pd.Series:
        """Return Series of average firing rates (Hz) keyed by flywire_id."""
        if self.last_rates_series is None:
            raise RuntimeError("No simulation has been run yet. Call simulate() first.")
        return self.last_rates_series

    def get_neuron_rate(self, neuron_id: int) -> float:
        """Get the firing rate (Hz) of a specific neuron."""
        if self.last_rates_series is None:
            return 0.0
        return float(self.last_rates_series.get(neuron_id, 0.0))

    def get_motor_neuron_rates(self) -> Dict[str, float]:
        """Convenience method returning firing rates for MN9 left and right proboscis extension motor neurons."""
        return {
            'MN9_left': self.get_neuron_rate(MN9_LEFT),
            'MN9_right': self.get_neuron_rate(MN9_RIGHT),
        }

    def get_per_trial_rates(self, neuron_id: int, duration_ms: float, n_trials: int) -> List[float]:
        """
        Calculate firing rate (Hz) for a specific neuron across each individual trial.
        """
        if self.last_spike_df is None or len(self.last_spike_df) == 0:
            return [0.0] * n_trials
        
        trial_s = duration_ms / 1000.0
        rates = []
        neu_spikes = self.last_spike_df[self.last_spike_df['flywire_id'] == neuron_id]
        
        for tr in range(n_trials):
            count = len(neu_spikes[neu_spikes['trial'] == tr])
            rates.append(count / trial_s)
        return rates

    def get_motor_neuron_stats(self, duration_ms: float, n_trials: int = 1) -> Dict[str, Dict[str, float]]:
        """
        Return mean, standard deviation, and per-trial rates for MN9 left and right proboscis extension motor neurons.
        """
        left_rates = self.get_per_trial_rates(MN9_LEFT, duration_ms, n_trials)
        right_rates = self.get_per_trial_rates(MN9_RIGHT, duration_ms, n_trials)
        
        return {
            'MN9_left': {
                'mean_hz': float(np.mean(left_rates)),
                'std_hz': float(np.std(left_rates, ddof=1)) if len(left_rates) > 1 else 0.0,
                'trials_hz': [float(x) for x in left_rates],
            },
            'MN9_right': {
                'mean_hz': float(np.mean(right_rates)),
                'std_hz': float(np.std(right_rates, ddof=1)) if len(right_rates) > 1 else 0.0,
                'trials_hz': [float(x) for x in right_rates],
            },
        }

    def get_active_neurons(self, min_spikes: int = 1) -> Set[int]:
        """Return the set of unique FlyWire IDs that fired at least min_spikes."""
        if self.last_spike_df is None or len(self.last_spike_df) == 0:
            return set()
        counts = self.last_spike_df.groupby('flywire_id').size()
        return set(counts[counts >= min_spikes].index)
