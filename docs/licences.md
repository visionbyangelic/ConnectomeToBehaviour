# Licences and data-use terms — on record at Part 1

**Why this file exists:** source register item 12 (added at Part 0 on Reviewer 2's verdict) requires the actual FlyWire data-use terms and the upstream repository's licence/attribution rules to be copied verbatim into the project record at download time — not paraphrased, not remembered. Both texts were fetched on **23 Nov 2026** from the sources named under each heading and are reproduced below exactly as published.

**What governs what, in one paragraph:** the *code and model files* in the upstream `philshiu/Drosophila_brain_model` repository are MIT-licensed (text 1). The *FlyWire data itself* — the published dataset from which the v630 completeness/connectivity files derive — is available under **CC BY-NC 4.0** per the FlyWire Principles (text 2): attribution required, non-commercial use. This project is non-commercial academic work, and every release artefact (Part 8) must carry the FlyWire attribution and cite Dorkenwald et al. 2024 and Shiu et al. 2024. The repo licence being MIT does **not** relicense the underlying FlyWire data.

---

## Text 1 — `philshiu/Drosophila_brain_model` repository LICENSE (MIT)

Source: https://raw.githubusercontent.com/philshiu/Drosophila_brain_model/main/LICENSE (fetched 23 Nov 2026; GitHub license API identifies it as MIT, blob SHA `deca2d0f1e82e910d8248b0d27398eb9450976ee`).

```
MIT License

Copyright (c) 2023 Philip Shiu and Nico Spiller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Text 2 — FlyWire Principles (the FlyWire data-use terms)

Source: https://edit.flywire.ai/principles.html (fetched 23 Nov 2026; page text reproduced in full below; the document is "Version 1.3 June 30, 2023"). Corroboration of the headline term, from https://flywire.ai/guidelines (checked 23 Nov 2026): "FlyWire's public release data is made available under license CC BY-NC 4.0", and the FlyWire Terms of Service (https://edit.flywire.ai/tos.html) bind use of flywire.ai to these Principles.

> ## FlyWire Principles
>
> *By the use of flywire.ai, you agree to be bound by these Principles and by the website Terms of Service.*
>
> ## Community principles
>
> *Access to the published dataset*. Published versions of FlyWire's data are available under CC BY-NC 4.0 license. The principles below describe how to approach usage of FlyWire for data that is not part of a public release yet or that was used before the data was made public.
>
> *Openness*. All results of proofreading are immediately available to all members of the FlyWire community. All researchers in fly neurobiology laboratories are welcome to apply.
>
> *Fairness*. Before using previously unpublished reconstructions in a presentation or scientific publication, users must obtain agreement from every lab that identified those cells or contributed more than 10% of the edits on those reconstructions, or assessed them to be adequately complete according to community standards. This applies to FlyWire cells themselves and also to the use of FlyWire data for any purpose. (For example, this applies to cells reconstructed in other EM software platforms using FlyWire data for guidance.) When contacting FlyWire users to seek their agreement for the use of cells they contributed to, a lack of response within one month may be taken as agreement. Contributors may request co-authorship or acknowledgments, with the understanding that a few hours or days of work may not constitute authorship, but that many days or months of work most likely would. In addition, it is important for the advancement of science that contributors not block publication for others - if a block to publication is requested, an appeal can be raised with the advisory board, who will consider factors such as research interests and relative contributions of the labs involved. Early and active collaboration between users is encouraged to prevent disputes.
>
> To publish neurons from FlyWire, a member lab must submit a list by emailing flywire@princeton.edu or through a planned online submission system, and then must make that list available in the paper. The list should include segment IDs plus coordinates of a point in each nucleus, or if no nucleus is present, a point in a main branch. Once FlyWire neurons are published, they are available for free use with appropriate citations, without soliciting the agreement of FlyWire users who contributed to the published versions of those neurons. (If a neuron is edited after publication, the use of its post-publication edited version is subject to the agreement of contributors as described for unpublished neurons above.)
>
> *Communication*. Labs are encouraged to communicate with each other early in a project through chat, email, and other channels. Coordination of reconstruction and analysis activities will increase the pace of discovery. Members may not share information with any individual who has not been granted access or agreed to these Principles. All active members and their PIs must sign onto the FlyWire Forum frequently to check for announcements and collaborative communications from other members.
>
> *Mutual respect*. We should all respect each others' efforts to achieve the common goal of understanding the fly nervous system. Mutual respect fosters a win-win situation, and generates synergy that lifts everybody up.
>
> ## Design principles
>
> *Wikipedia-style crowd wisdom*. Anyone is permitted to edit anything. We believe this approach will yield accuracy, once we find the appropriate checks and balances.
>
> *Social before technological solutions*. Prototyping of workflows should focus on getting the human element right, using "low-tech" means like Google Docs and Sheets for coordination. Later on, workflows will be implemented by engineering team as integrated features of the FlyWire site.
>
> *Cultural norms over formal laws*. The FlyWire community should establish a good culture from the outset. Formal laws will be introduced when necessary but ideally will be kept to a minimum.
>
> Version 1.3 June 30, 2023

---

## Gaps and limits of this record (stated, not hidden)

- The Principles text above was captured from the page's rendered text on 23 Nov 2026; if FlyWire republishes the Principles (the version on record is v1.3, 30 June 2023), this file should be refreshed and the change logged — the terms that matter at *release* time (Part 8) are the ones then in force.
- The FlyWire Terms of Service proper (edit.flywire.ai/tos.html) govern use of the *website*; this project does not use the website interactively, so the Principles (which the ToS incorporate by reference) are the operative data terms and are what is copied here. The ToS page exists and was identified; its full text was not copied, because it binds site use rather than the published dataset this build consumes.
- Nothing in either text licenses the *derived simulation outputs of this project* — those are the project's own, with the CC BY-NC 4.0 attribution duty for the FlyWire data they derive from carried into every release artefact.
