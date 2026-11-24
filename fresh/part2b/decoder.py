"""The Part 2b TOY decoder: descending-neuron spikes -> body command.

TOY / PROVISIONAL -- this decoder exists to prove the brain-to-body
interface, not to be the Part 4/5 decoder. It is replaced there. Every
document that mentions it must say so.

What it does, in full (there is nothing else in it):

1. INPUT: the pooled spike count of the descending readouts
   (aDN1 + aDN2-left, the DN populations of the Part 2 ID sets) over one
   brain chunk, and the chunk duration. The "population rate" is the
   summed count divided by the duration -- for a two-neuron readout set,
   spikes/second summed across the set is the honest population signal;
   a per-neuron average would just rescale the thresholds below.
2. FILTER: an exponential moving average of that rate, time constant
   TAU_S. One chunk of a two-neuron readout is a handful of spikes, so
   the raw rate is mostly Poisson noise; the filter is the windowing
   choice, and its lag (~TAU_S) is part of the loop's documented delay.
3. MAP: a clipped linear ramp from rate to command amplitude:
   amplitude = clip((rate_ema - R_ON) / (R_SAT - R_ON), 0, 1).
   R_ON and R_SAT are CHOSEN values (see below), not fitted ones.
4. OUTPUT: the body's 2-vector descending signal (left, right) =
   (amplitude, amplitude). Symmetric, because it cannot honestly be
   anything else: the extracted DN sets contain aDN1 (a single unpaired
   neuron) and aDN2-left only -- there is no right-side DN in the sets,
   so any left/right difference in the command would be invented, not
   decoded. Straight walking is what this decoder can say.

Chosen constants, with their reasons (Part 4/5 must re-derive or fit
their own on calibration data; these are for interface proof only):

- R_ON = 2 Hz: just above silence. The DNs fire exactly 0 spikes in
  30 sugar-only trials (Part 3 output), so the floor only has to clear
  numerical zero, not a biological baseline.
- R_SAT = 40 Hz (pooled): two DNs firing ~20 Hz each saturate the
  command. Whether JON drive actually recruits the DNs to that level is
  an empirical question the probes answer; if it does not, the loop
  result is reported as it comes out, not rescued by retuning here --
  retuning the decoder on the loop's own outcome is exactly the
  calibration/evaluation confusion the plan forbids (FINAL-PLAN S7.3).
- TAU_S = 0.2 s: two chunks of smoothing at the 100 ms chunk cadence.

Bridge-test properties (checked in tests/test_decoder.py): zero input
gives exactly zero command, the map is monotone and saturating, and
left == right always.
"""

import math

R_ON_HZ = 2.0
R_SAT_HZ = 40.0
TAU_S = 0.2


class ToyDecoder:
    """Stateful toy decoder (the state is the rate filter, nothing else)."""

    def __init__(self, r_on=R_ON_HZ, r_sat=R_SAT_HZ, tau=TAU_S):
        if not r_sat > r_on >= 0:
            raise ValueError("need r_sat > r_on >= 0")
        if tau <= 0:
            raise ValueError("need tau > 0")
        self.r_on = float(r_on)
        self.r_sat = float(r_sat)
        self.tau = float(tau)
        self.rate_ema = 0.0

    def reset(self):
        self.rate_ema = 0.0

    def update(self, dn_spike_count, duration_s):
        """Advance one chunk. Returns (amplitude, rate_inst, rate_ema).

        dn_spike_count -- pooled aDN1 + aDN2-left spikes in the chunk.
        duration_s     -- the chunk's simulated duration in seconds.
        """
        if duration_s <= 0:
            raise ValueError("chunk duration must be positive")
        if dn_spike_count < 0:
            raise ValueError("spike count cannot be negative")
        rate_inst = dn_spike_count / duration_s
        # Discrete EMA with the exact exponential weight for this step,
        # so the filter means the same thing if the chunk size changes.
        alpha = 1.0 - math.exp(-duration_s / self.tau)
        self.rate_ema += alpha * (rate_inst - self.rate_ema)
        frac = (self.rate_ema - self.r_on) / (self.r_sat - self.r_on)
        amplitude = min(1.0, max(0.0, frac))
        return amplitude, rate_inst, self.rate_ema

    def signal(self, dn_spike_count, duration_s):
        """The body's descending 2-vector for this chunk: (left, right)."""
        amplitude, _, _ = self.update(dn_spike_count, duration_s)
        return (amplitude, amplitude)
