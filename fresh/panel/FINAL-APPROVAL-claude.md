# Final approval — Claude (Reviewer 1, lead)
Chat: https://claude.ai/chat/e3e2b04f-0f06-4905-bb69-f068f549879b
Free tier, signed in as "Nerdy · Free". FINAL-PLAN.md uploaded in full (398 lines); Claude read the whole file, not a summary. Approval message sent with the file attached at ~16:07 WAT, 23 Nov 2026.

## Round 1 — 23 Nov 2026, ran 16:03-16:09 WAT (browser task, ~6 min)
Verdict: **NO as written — conditional YES. Three required edits; "None changes the science or the design. Once they are made, my answer is yes."**

He also spot-checked one citation chain: the BANC reference (Bates, Phelps, Kim, Yang et al., Nature, published 8 June 2026, DOI 10.1038/s41586-026-10735-w, one adult female, densely reconstructed) matches primary and institutional sources. He did not re-check the MaleCNS Cell citation or the Eon quotations; for those he relies on RESEARCH-CHECK.md, which he has not seen.

### Required change 1 — E-Baseline estimand (§2.1, §5.1, §5.6, §7.6)
The main question compares intact vs "connectome-free baselines and controllers run through the identical body", but E-Total is defined only against null families and E-Pathway only for lesion vs matched control. The rule baselines (C1–C3) and body-only baselines had no named estimand or primary metric, while §5.6's convincing-positive criteria and §7.6's permitted-conclusions table both depend on "intact vs baselines". Fix: add a third named estimand (E-Baseline) — intact-vs-baseline difference on the held-out evaluation set, through the identical body, for the fixed-implementation and capability tests separately, with primary metric and TOST bounds named the same way as the other two.

### Required change 2 — Sensory pathway specs vs the first loop (§4, Part 2b, Part 4, §7.2)
§7.2 said specs are "pre-registered at Part 4 and reviewed by the panel before the loop is built", but Part 2b builds a loop before Part 4 and cannot run without some definition of the sensory events. Fix: Part 2b uses provisional specs labelled exploratory and non-binding; final specs are pre-registered at Part 4 and panel-reviewed before Part 5's real decoder runs; §7.2 to say "before the Part 5 loop", not "before the loop is built".

### Required change 3 — Human expert check has no fallback (§0.2(c), D6, Part 0, §8 item 6)
D6 and §8 treat ≥1 human expert check (at pre-registration and at the final gate) as the safeguard against shared AI blind spots, but Part 0 only says "sought" and its pass criteria do not require it — if no expert is found, nothing stops the pre-registration freeze. Fix: at the Part 5 pre-registration freeze, either the expert check is on record, or Angelic signs a logged waiver stating the mitigation was not obtained. Same rule at the final gate.

### Housekeeping (not blocking, fixed in the same pass)
- §10.1 "There is no newer whole-brain LIF model that supersedes it" as a flat claim → reword as "to our knowledge as of 23 Nov 2026" and point to the search protocol in RESEARCH-CHECK.md (a negative from search is weak evidence; §11.4 already dates its comparable claim).
- §4 and §5.6 refer to "Part 7b" (the walk/halt repeat), which is not a row in the parts table → add it as a row. (Note: on re-check, "Part 7b" appears only in the §4 Part 7 row; the row was added there.)
- §0.3 and §12 still say final approval is pending, which is stale → update from the real records in panel/FINAL-APPROVAL-*.md once those exist.
- §2.1's annotation says "which §2.1 below forbids", but the prohibition is in the paragraph that follows it within the same section → say "the next paragraph".

### Interaction with the other approvals
Gemini and ChatGPT approved the earlier text; these edits change the document they approved. Under the plan's own no-quiet-changes rule, log them as an amendment. Ask the other two to confirm only the changed lines, not re-review the whole plan. Claude: "If the amendments are made as described, I approve the plan. I do not need to re-read it in full, only the edited passages."

## Amendments applied — 23 Nov 2026 (Buddy)
All three required changes + all four housekeeping items applied to FINAL-PLAN.md (399 lines after amendment; was 398):
1. **E-Baseline (§2.1):** main question now names E-Baseline; "Three estimands are pre-registered"; E-Baseline defined as the intact-vs-baseline difference (rule baselines C1–C3 + body-only/decoder-only baselines), identical body, held-out evaluation set, fixed-implementation and capability tests separately; primary metric = the behaviour's pre-registered primary endpoint (§5.2); TOST bounds per metric as for the other two. Plain-words paragraph updated to three ways. **§5.1:** E-Baseline added to the estimand list. **§5.6:** TOST bounds now stated for E-Total, E-Pathway **and E-Baseline** alike. **§7.6:** outcome table now labels each comparison (E-Total / E-Baseline / E-Pathway).
2. **Part 2b provisional specs (§4 Part 2b row):** "Sensory events in 2b use provisional specs, labelled exploratory and non-binding; the final sensory pathway specs are pre-registered at Part 4 (§7.2) and must be panel-reviewed before the Part 5 loop runs." **§7.2:** now reads "reviewed by the panel before the Part 5 loop is built" with the provisional-spec note. **§4 Part 0 row:** waiver-rule pointer added.
3. **Expert-check fallback (§0.2(c)):** "at the Part 5 pre-registration freeze, either the expert check is on record, or Angelic signs a logged waiver stating the mitigation was not obtained; the same rule applies at the final gate (Part 8)". **§8 item 6:** fallback added with the same wording. **D6:** waiver rule added to the recommended choice.
4. **Housekeeping:** §10.1 reworded to "to our knowledge as of 23 Nov 2026" with pointer to RESEARCH-CHECK.md (32 claims checked 23 Nov 2026) and the dated-not-absolute note. New **Part 7b row** added to the §4 parts table (walk/halt repeat, Core-B, HARD, own pre-registration). §2.1 annotation now says "which the next paragraph forbids". §0.3/§12 pending-language update deferred to the approval-completion step (after all three reviewers' records exist), per Claude's own condition.

Consistency check (per task): all three required changes are additions to the plan's existing rigour machinery (estimands, exploratory labelling, gate discipline) — none changes the science, design, questions, scope, or the FRESH-START-PROTOCOL.md rules, and none contradicts Gemini's or ChatGPT's approvals (both approved the same estimand/pre-registration framework these edits complete).

## Round 2 — re-ask (same chat, edited passages only) — 23 Nov 2026, ran 16:13-16:16 WAT (browser task, ~3 min)
Amended FINAL-PLAN.md (399 lines) uploaded (shown as FINAL-PLAN_1.md in the chat, since a file of that name was already there); re-ask message with the edited passages sent ~16:14 WAT. Claude read the edited passages in the attached file, not the summary.
Verdict: **YES — APPROVED as amended.** "Yes, I approve the plan as amended." He verified each edit in the file: E-Baseline named with the comparison set (rule baselines C1–C3 + body-only/decoder-only baselines), held-out evaluation set, identical body, fixed-implementation and capability tests separate, primary metric = pre-registered endpoint, TOST bounds covering all three estimands, §7.6 table keyed to all three; Part 2b specs provisional/exploratory/non-binding with final specs pre-registered at Part 4 and panel-reviewed before the Part 5 loop; waiver rule present in §0.2(c), §4 Part 0, §8 item 6 and D6; housekeeping all present (§10.1 dated/hedged, Part 7b a real row, §2.1 annotation "the next paragraph").

Two small non-blocking follow-ups, neither requiring re-reading:
1. Part 7b's gate class: marked HARD in its row but §0.2(c)'s HARD list read "Parts 0, 3, 5, 6, 7" → **fixed 23 Nov 2026** (list now "Parts 0, 3, 5, 6, 7, 7b"). This fix is included in the changed-lines set sent to Gemini and ChatGPT for confirmation.
2. §0.3 and §12 still describe final approval as pending → to be updated from the real panel records once Gemini + ChatGPT confirm the changed lines (see FINAL-APPROVAL-STATUS.md).

Limits of this approval (Claude's own words, in substance): covers the plan's internal consistency and design logic. He spot-checked BANC against primary sources and relied on RESEARCH-CHECK.md for the other citations and the Eon quotations, which he has not seen. Because these edits change the text Gemini and ChatGPT approved, log them as an amendment under the plan's own rule and ask the two of them to confirm only the changed lines — in progress, see FINAL-APPROVAL-STATUS.md.
