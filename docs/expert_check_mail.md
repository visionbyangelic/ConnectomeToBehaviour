# Expert check — the mail (rewritten again 24 Nov 2026: plain language from zero, every choice explained so the reader — and Angelic — can follow it fully)

**Subject:** My fly-brain feeding simulation — can you tell me if my choices are wrong?

---

Hi [Name],

I'm Angelic, a final-year Computer Science student working on computational neuroscience. I've built a simulation I want to explain properly, because I'm about to run the main experiment and I'd like someone in this field to tell me if any of my choices are wrong before I do. Everything is in this mail.

**What I built.** Scientists have mapped the complete wiring of a fruit fly's brain — all 127,400 neurons and every connection between them. I turned that map into a living simulation: the neurons fire, signals travel along the real wiring. Then I connected the simulated brain to a simulated fly body, so the brain can actually *do* something instead of just firing in a void. The behaviour I chose is feeding.

**How feeding works in my setup.** When a real fly tastes sugar, sensory neurons on its mouthparts fire, the signal travels through the brain, and it reaches two motor neurons (called MN9, one on each side) that push out the fly's feeding tube, the proboscis, so it can drink. My simulation copies that path: I stimulate the sugar-sensing neurons, the signal travels through the simulated brain, MN9 fires, and a "decoder" turns MN9's firing into movement of the fake proboscis. When the proboscis touches the food, a signal goes back into the brain — that return signal is my construction, built from the moment of contact, because the simulated body has no sense of taste of its own. The loop is closed: taste in, movement out, contact back in.

**What I've already checked.** Before trusting any of this, I tested the brain on its own: stimulating the sugar neurons in my model produces almost exactly the firing pattern of the published model it's based on (Shiu et al., *Nature* 2024) — the firing rates match with a correlation of 0.999. Checking that closely turned up something small but real: their published results were generated with the sensory neurons driven at 200 pulses per second, even though their code's default says 150. I use 200, because that's what their data shows.

**The experiment I'm about to run.** I block the outgoing signals of a chosen group of neurons — the neurons still fire as normal, but their messages never reach anything downstream, like cutting the wires leaving a room while the people inside keep talking. Then I watch whether feeding changes. I do the same thing to other groups of neurons as controls, so I can tell whether the effect belongs to that specific group or would happen with any similar group.

**The choices I need checked.**

*The neurons.* The input is the sugar-sensing neurons on the right side only — 21 of them — because the published benchmark used exactly that set, so my validation rests on it. Bitter (21 neurons) and water (18) give me the other taste conditions. The readout is MN9, because it is the final step: if feeding happens at all, it happens through those two neurons. I always report the left and right MN9 separately, because they don't respond equally — under sugar the left fires about 93 times a second, the right about 62 — and merging them would hide that.

*Blocking outputs, not deleting neurons.* Deleting neurons would change the structure of the network itself. Blocking only their outgoing signals leaves the network intact and stops just their influence, which is the cleaner question: not "what if these neurons didn't exist" but "what if nothing could hear them."

*The controls.* For each targeted group, I built five control groups, matched to it on four things: how many connections they receive, how many they send, their total number of synapses, and whether they mostly excite or inhibit their targets, plus how active they are in normal runs. One gap I'll state plainly: the controls are **not** matched on which brain region the neurons sit in. The neuron lists come from the published paper, which doesn't record region for these sets, and I don't have a reliable region label for them. So if region matters, my controls don't rule it out, and I say so wherever I report results.

*The decoder rule.* The body needs one number: how much MN9 firing counts as "proboscis fully extended." I set that number from the brain's own normal response to sugar — the firing level it reaches or exceeds only 5% of the time once it has settled — measured in separate runs done only for this, and then locked. It cannot be adjusted after the experiments, so I can't tune it to make any result come out better.

*The body.* Two simulated bodies exist. I chose FlyBody, because in the other one (NeuroMechFly) the mouthparts are drawn but cannot actually be driven by signals — the loop could never close. One honest consequence of my setup: with the head held still, the proboscis stops about a quarter of a millimetre short of food sitting on the ground, so in my arena the food sits on a tiny platform, a third of a millimetre high. That's an arena choice I made so contact is possible at all — it is not a finding, and I state it wherever I report feeding.

*The numbers.* Each condition gets 20 runs, because the stimulation is partly random and every run differs slightly. And I decided in advance what "the same" means: if blocking a group changes the response by more than ±25%, I report a difference. If it lands inside ±25%, I call it equivalent. If the runs are too noisy to tell, I say inconclusive. What I never do is call a blurry result "no effect."

**My questions.** Do the neuron choices look right? Are the controls fair, given the region gap? Is ±25% a reasonable line for this kind of data? And is there anything the field already knows that makes one of these choices wrong?

Even a few lines would help — if one choice looks weakest, just pointing at it is enough. Thank you for reading.

Angelic
