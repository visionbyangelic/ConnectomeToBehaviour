"""The Part 2b sensory-return channel: leg contact -> brain event.

PROVISIONAL / CONSTRUCTED -- the body has no mechanosensory organ the
brain model can hear; this channel is the Part 2b stand-in for one, and
it is labelled that way everywhere. The final sensory pathway specs are
pre-registered at Part 4 (FINAL-PLAN S7.2); nothing here binds them.

The channel, defined exactly:

- The body reports, at every physics step, one ground-contact flag per
  leg (MuJoCo contact sensors, via FlyGym's get_ground_contact_info).
- A TRANSITION is a leg whose flag differs from the previous physics
  step (touchdown or liftoff). Standing still produces no transitions
  once the fly has settled; walking produces them continuously, because
  stepping is legs cycling between stance and swing.
- The bridge rule (in run_loop.py): if a body chunk contains at least
  one transition, the brain's JON population -- the mechanosensory
  Johnston's-organ neurons, whose descending readouts are exactly the
  aDNs the toy decoder reads -- is driven for the whole of the NEXT
  brain chunk. One chunk of feedback latency, stated, not hidden.

Why transitions and not contact level: a level signal would be ON for
the entire episode (a standing fly is in contact too), so it could not
demonstrate that body *events* re-enter the brain. Transitions are
events, they are caused by movement, and they stop when movement stops
-- which is what makes the open-loop control episode (feedback logged
but not converted) a meaningful contrast.
"""


class ContactTransitions:
    """Counts per-leg contact-flag transitions across physics steps."""

    def __init__(self, n_legs=6):
        self.n_legs = n_legs
        self._prev = None
        self.total = 0

    def reset(self):
        self._prev = None
        self.total = 0

    def set_baseline(self, flags):
        """Establish the current flags without counting transitions
        (used once after warmup, so settling is not counted as events)."""
        flags = [bool(f) for f in flags]
        if len(flags) != self.n_legs:
            raise ValueError(f"expected {self.n_legs} contact flags, "
                             f"got {len(flags)}")
        self._prev = flags

    def update(self, flags):
        """Feed one physics step's flags; returns transitions this step."""
        flags = [bool(f) for f in flags]
        if len(flags) != self.n_legs:
            raise ValueError(f"expected {self.n_legs} contact flags, "
                             f"got {len(flags)}")
        if self._prev is None:
            self._prev = flags
            return 0
        n = sum(1 for a, b in zip(flags, self._prev) if a != b)
        self._prev = flags
        self.total += n
        return n
