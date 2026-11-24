# Part 1 gate review — LIGHT gate

- **Gate:** Part 1 (Environment + data) — LIGHT gate, per the plan's two-gate design (D6).
- **Rotating reviewer:** Reviewer 3.
- **Date/time:** 23 November 2026, ran 19:50–19:52 WAT (free tier, existing chat).
- **Verdict: APPROVED — the Part 1 gate can close**, subject to Angelic's summary sign-off (the standing second half of every LIGHT gate).

## What the reviewer accepted

- **The sugarR verdict (TRUSTED) is upheld** — trusted as the Part 3 benchmark in its correct role: Shiu et al.'s *model-output* benchmark, **not** biological ground truth. Matching it at Part 3 will prove the model was reproduced, nothing more, and the review accepts the verdict on that basis. Reviewer 3's note: the file's SHA-256 and its upstream provenance must remain in the Part 1 manifest — they are, in `fresh/PART1-DATA.md` (SHA-256 for all three v630 files, download procedure and post-move re-verification recorded there). Condition satisfied as stated.
- **Brain environment and the numpy pin** — accepted (Brian2 2.9.0 / numpy 1.26.4 and the two-isolated-environments resolution of the brain-vs-body numpy conflict).
- **The pyarrow pin-down** (26.0.1 → 20.0.0, because 26.x demands numpy ≥2) — accepted as properly documented: a logged deviation with its reason, not a silent change.
- **Python 3.12** — accepted *provisionally*, as a recorded reproducibility deviation from the upstream model's original environment, on the record rather than assumed away.
- **The benchmark re-run** in the pinned environment — accepted (full scale 9.7–10.9 s per 100 ms, confirming the Part 0 indicative numbers; GPU gate stays closed).
- **The v630 ID-set equality check** — the connectivity and completeness ID sets being exactly equal was called **a strong integrity check** on the data.
- **Licences** — accepted, with the distinction preserved: the upstream model code is MIT; the FlyWire published data is CC BY-NC 4.0; the code licence does not relicense the data (`fresh/LICENCES.md`).
- **The v630 materialisation as the identity source of record** — accepted (current annotation releases are v783-era and interpretive-only for v630; the exact annotation pin is deferred to Part 2 reading, with reason recorded).

## Boundary warning (recorded verbatim in substance)

The body-environment smoke test (FlyGym/MuJoCo imports pass, a minimal model steps headless) is **not** body-capability evidence. What the body can actually do — which behaviours it can honestly support — belongs to the **Part 1b audit**. Part 1 must never be cited as proving body capability.

## Carry-forward: formal Part 2 obligation (Reviewer 3's wording, in substance)

> **Part 2 obligation — neuron identity extraction:** extract and independently cross-check the GRN, MN9 and DN neuron ID sets using the v630 materialisation and the selection logic in model.py. Record the extraction method, source references, counts and resulting ID-set artefacts. Complete before using those populations in sensory-pathway specification, decoder construction or intervention experiments.

**Conditions attached:**
1. It is a **named obligation** of Part 2, not an informal intention.
2. The cross-check is **two-way against the v630 source material** — the sets are not merely copied out of `model.py`.
3. The ID-set artefacts are **recorded and versioned**.
4. **No premature use** of the GRN/DN sets (sensory-pathway specification, decoder construction, intervention experiments) before the obligation is complete.
5. Any mismatch found is **investigated and recorded, never silently resolved**.

This obligation is also entered in `~/workspace/connectome-work/WORKING-PLAN.md` as a Part 2 entry obligation.

## Gate state after this review

Reviewer's half of the LIGHT gate: **passed**. The gate closes on Angelic's summary sign-off.
