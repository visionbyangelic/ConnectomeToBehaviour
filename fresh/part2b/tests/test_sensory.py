"""Tests for the contact-transition counter: standing still is silent,
stepping is loud, and the baseline cannot manufacture events."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sensory import ContactTransitions  # noqa: E402

DOWN = [True] * 6
UP = [False] * 6


def test_standing_still_produces_no_transitions():
    c = ContactTransitions()
    c.set_baseline(DOWN)
    for _ in range(1000):
        assert c.update(DOWN) == 0
    assert c.total == 0


def test_first_update_only_sets_the_baseline():
    c = ContactTransitions()
    assert c.update(UP) == 0       # nothing to compare against yet
    assert c.update(DOWN) == 6     # now all six legs changed at once


def test_tripod_stepping_counts_six_transitions_per_cycle():
    # Tripod gait: legs alternate in two groups of three. One full
    # cycle (group A lifts while B lands, then back) = 12 transitions.
    c = ContactTransitions()
    a_down = [True, False, True, False, True, False]
    b_down = [False, True, False, True, False, True]
    c.set_baseline(a_down)
    assert c.update(b_down) == 6
    assert c.update(a_down) == 6
    assert c.total == 12


def test_wrong_number_of_legs_raises():
    c = ContactTransitions()
    for bad in ([True] * 5, [True] * 7):
        try:
            c.update(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("wrong leg count should have raised")
