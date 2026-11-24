# First loop: the minimal end-to-end loop (Part 2b)

My first brain-to-body loop, built early on purpose: the old build left
the bridge until last and never finished it, so here the link is proven
in its simplest form before anything else is built on top of it. The
full record is `docs/first_loop_build.md`.

## The loop

```
sugar stimulus (200 Hz, the Part 3 protocol, always on)
        |
   frozen brain (brain_model, Part 2/3)  -- 100 ms chunks, one persistent
        |                            Brian2 Network, JSON-lines bridge
   aDN1 + aDN2-left spike counts
        |
   TOY decoder (decoder.py)  -- pooled rate, EMA filter, clipped ramp;
        |                        PROVISIONAL, replaced at Parts 4/5
   descending 2-vector (amplitude, amplitude)
        |
   audited body pathway (Part 1b): HybridTurningController -> CPG ->
   preprogrammed steps -> NeuroMechFly legs
        |
   leg ground-contact transitions (sensory.py)
        |
   JON mechanosensory drive in the NEXT brain chunk
   (PROVISIONAL / CONSTRUCTED sensory channel; final specs at Part 4)
```

A scripted 200 ms "touch" pulse of JON drive at t = 0.2-0.4 s starts
each episode: the encoder-side stimulus that gives the feedback loop
something to sustain. One control episode runs with the feedback path
logged but never connected, to show what the loop itself contributes.

## Files

| File | What it is |
|---|---|
| `decoder.py` | The toy decoder (pure Python). |
| `sensory.py` | Contact-transition counting (pure Python). |
| `protocol.py` | The JSON-lines bridge contract both processes share. |
| `brain_worker.py` | Brain-env process: holds the frozen brain, runs chunks. |
| `run_loop.py` | Body-env driver: one closed- or open-loop episode. |
| `sanity_decoder_only.py` | Decoder-only sanity run (synthetic rates, no brain). |
| `run_battery.py` | The whole battery + the pre-set stability criteria. |
| `probes/` | The mechanism probes run before the loop was built (toggle, chunk equivalence, JON recruitment) + their results. |
| `tests/` | Decoder / sensory / protocol tests (16 tests). |
| `../../results/first_loop/` | Episode logs, sanity output, battery summary (JSON). |

## Running it

```
# tests (pure modules; the brain env carries pytest)
~/workspace/connectome-work/envs/brain/bin/python -m pytest tests/ -q

# the whole battery (body env; spawns the brain env itself)
~/workspace/connectome-work/envs/body/bin/python run_battery.py
```

Nothing here modifies the frozen model: `src/brain_model/` is imported,
never edited, and the loop's git status over `src/brain_model/` stays empty.
