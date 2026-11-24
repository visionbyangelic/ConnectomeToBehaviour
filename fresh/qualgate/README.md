# Feeding-body qualification gate — scripts

These are the scripts that execute the qualification gate specified in
`fresh/PART4-SENSORY-SPECS.md` §7, against the FlyBody model shipping inside
the pinned FlyGym 2.1.1 in `envs/body`. The gate record itself lives in
`fresh/FEEDING-BODY-QUALIFICATION.md`; machine-readable per-step results land
in `results/` next to these scripts.

- `q0_verify_artefact.py` — Q0: re-hash the five pinned model files and
  compare against §7.1 before anything runs.
- `q1_upstream_integrity.py` — Q1: replay the packaged FlyBody single-step
  assets through the packaged `FlyBodyPreprogrammedSteps` class on the pinned
  body, and record the state of the `muscle_imitation` sub-item.

Nothing in here adjusts a body parameter. That is deliberate: adjusting any
body parameter during the gate is an automatic gate failure (§7), so these
scripts only ever *command* the published actuators within their published
ranges and *measure* what the body does.
