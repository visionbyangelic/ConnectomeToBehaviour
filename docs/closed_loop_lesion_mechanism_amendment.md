# Amendment to the closed-loop code: the lesion mechanism for Part 7

27 Nov 2026.

The preregistration (section 8) registers Part 7 lesions as block_output on named neuron IDs, applied to the brain from before t = 0. But the closed-loop code had no lesion hook: loop_protocol.validate_scenario dropped any lesion key when it built the normalized scenario, and brain_worker.py never called brain.block_output(). The mechanism existed one layer down (Brain.block_output in the brain model, already used by the brain-only runner), but the closed loop could not reach it. The 12 lesion configurations could not run. This amendment adds the missing hook. It changes the code only; it does not change the preregistration text, and it does not alter the characterisation code or results. It applies to Part 7 going forward only.

## What I added

1. src/closed_loop/loop_protocol.py: the scenario gains an optional "block_output" field, a list of FlyWire neuron IDs, the same key the brain-only runner uses. validate_scenario checks it (must be a list of integers; absent or empty means no lesion) and preserves it in the normalized scenario dict, so run_loop5.py records it in the manifest automatically. No existing field's validation changed, and a scenario without the key normalises exactly as before.

2. src/closed_loop/brain_worker.py: in start(), after brain.build() and before the compile warmup, if the scenario carries a non-empty block_output list, the worker calls brain.block_output(lesion_ids). The lesion IDs and the number of synapses zeroed are recorded in the "ready" reply and in stderr (so brain_worker.log records them). When no lesion is present, the worker calls nothing and the existing flow is unchanged. The lesion is applied before the compile warmup so the compiled model includes the zeroed synapses.

## Verification

I re-ran the INT seed 5200 episode under the new code to a temporary directory, with the same scenario file and the same seeds. The brain_log.jsonl and body_log.jsonl are bit-identical to the existing run (same SHA-256 for both files). The manifest differs only in the git working-tree state (the two modified files, and the pre-existing untracked Part 7 results directory now containing files) and in wall-clock time (113.6 s against 129.1 s); every substantive field (scenario, seeds, r_hi, gating, validity, pilot, settle, rest pose, worker ready, data hashes) is identical, and the summary's scientific numbers match exactly (peak E 2.0575192780092904, first contact chunk 14, event ON 86 chunks, total MN9 spikes 1591). The existing INT seed 5200 episode stands, because the no-lesion code path is unchanged and the logs are bit-identical.

I ran a lesion smoke test: one episode with block_output on the two MN9 IDs. It completed (VALID, 100 chunks). The manifest records the lesion IDs in the scenario, and brain_worker.log records "lesion applied: block_output IDs [720575940660219265, 720575940645521262], 158 outgoing synapses zeroed". I also ran a second smoke test blocking the 21 sugar GRN right IDs: it completed, the log records 1547 outgoing synapses zeroed, and the MN9 counts in brain_log.jsonl are exactly zero, with peak E near zero and no contact. Both smoke-test directories were deleted afterwards; neither is a Part 7 episode.

The analysis code self-test passes.

## What the smoke test showed about block_output

Blocking the two MN9 IDs does NOT zero the MN9 spike counts (1574 spikes, against 1591 intact). That is the registered mechanism working as specified, not a failure of the hook: Brain.block_output zeroes the neurons' outgoing synaptic weights, and the neurons keep receiving input and keep spiking; their spikes simply stop doing anything downstream. The MN9 lesion did change the episode (first contact chunk 5 against 14, event ON 95 chunks against 86, final E 1.835 against 2.014), through the changed brain dynamics. And the decoder reads MN9 spikes directly from the spike monitor, not through synapses, so an MN9 lesion does not abolish extension by itself. I record this here so the L-MN9 episodes are read correctly: the lesion zeroes MN9's outgoing synapses inside the brain, and the MN9 spike counts are not the measure of whether it took effect; the synapse count in the log is. The GRN smoke test shows the complementary case: blocking the upstream drive zeroes the downstream MN9 readout exactly.

## Note on the manifest

The lesion IDs reach the manifest through the scenario (manifest["scenario"]["block_output"]), which run_loop5.py records automatically. The synapse count is in the ready reply and in brain_worker.log. The manifest's worker_ready block copies only three fields from the ready reply (populations, data_hashes, declared_drives), so the synapse count does not appear there; recording it there would need a change to run_loop5.py, which is outside this amendment's two files.

## Code hash

Pre-amendment SHA-256: src/closed_loop/loop_protocol.py 6f8973e791afbdcbf79794ae276f2ccd9872f7d2b8c79763d6ad91fce3ab77c6; src/closed_loop/brain_worker.py ef254c96b69fba6c97e9734984567ba328194c9ad7aca92cf1400c2f0f4eaf57. Post-amendment SHA-256: src/closed_loop/loop_protocol.py 80eae96f288e56abf16605ebf7e0698b1e53d3b484a1642bdcacb52725c8ef1b; src/closed_loop/brain_worker.py f400d708dc1f40bb4464ab0deead2548ffe425e300f6637f516503ff2096f043. The amendment is recorded by these hashes.
