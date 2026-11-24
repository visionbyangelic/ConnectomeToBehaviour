"""Tests for the Part 2b toy decoder -- the bridge-test properties the
plan asks of any decoder (FINAL-PLAN S6.2), applied to the toy:
zero input -> zero command; monotone; saturating; symmetric."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from decoder import ToyDecoder  # noqa: E402


def test_zero_input_gives_exactly_zero_command():
    d = ToyDecoder()
    for _ in range(50):
        amp, rate_inst, _ = d.update(0, 0.1)
        assert rate_inst == 0.0
        assert amp == 0.0
    assert d.signal(0, 0.1) == (0.0, 0.0)


def test_signal_is_always_symmetric():
    d = ToyDecoder()
    for count in (0, 1, 3, 6, 20, 100):
        left, right = d.signal(count, 0.1)
        assert left == right


def test_map_is_monotone_and_saturates():
    # Fresh decoder per level so the EMA starts from zero each time;
    # run long enough (10 s) for the filter to settle at each level.
    amps = []
    for rate_hz in (0, 5, 10, 20, 40, 80, 200):
        d = ToyDecoder()
        amp = 0.0
        for _ in range(100):
            amp, _, _ = d.update(rate_hz * 0.1, 0.1)
        amps.append(amp)
    assert amps == sorted(amps), f"not monotone: {amps}"
    assert amps[0] == 0.0
    assert amps[-1] == 1.0
    assert 0.0 < amps[3] < 1.0  # 20 Hz pooled sits mid-ramp, not at a rail


def test_filter_smooths_a_single_chunk_of_noise():
    # One loud chunk must not slam the command to full. A loud chunk
    # for a two-neuron readout is ~4 spikes (40 Hz pooled); with
    # tau=0.2 s and a 0.1 s chunk the EMA moves only ~39% of the way
    # toward it, so the amplitude stays well below saturation.
    d = ToyDecoder()
    amp, _, _ = d.update(4, 0.1)
    assert 0.0 < amp < 0.6


def test_reset_clears_the_filter():
    d = ToyDecoder()
    for _ in range(20):
        d.update(10, 0.1)
    assert d.rate_ema > 0
    d.reset()
    assert d.rate_ema == 0.0


def test_bad_inputs_raise():
    d = ToyDecoder()
    for bad in ((-1, 0.1), (1, 0.0), (1, -0.1)):
        try:
            d.update(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"update{bad} should have raised")
