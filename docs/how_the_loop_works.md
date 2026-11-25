# How the loop works, in plain words

This is my own plain words record of how the closed loop works, written so I can explain it without notes. It covers the Part 5 feeding loop: the brain, the body, the translator between them, and what the pictures from the runs show and do not show.

## What the pictures are

The pictures and videos from the Part 5 runs are drawings of recorded data, not camera recordings of a real fly. The fly's shape comes from the published FlyGym body model. Its movement comes from the joint angles recorded during the actual episode run, replayed exactly: the largest difference between the replay and the record is 0.00 rad. No image generator was used anywhere in them. The numbers are the evidence. The pictures are only for looking at, and every caption file says so.

## The parts in the picture

The fly is the FlyBody model: a simulated fruit fly body with a working mouth (the proboscis) and legs, run inside the MuJoCo physics engine.

The pale shape under the head is the fly's mouth, the labrum. It is part of the fly, not food. It is pale cream in the model's own colours, and it hangs under the head even at rest, so in a still frame it can look like a separate white thing the fly is holding. It is not. The labelled rest frame (results/closed_loop/stills/arm_a_seed5111_rest_labelled.png) shows it next to the food with a gap between them.

The food is the amber disc. The amber colour is a render only choice so the food reads as food. The disc sits on a grey pedestal, a raised surface. I state this plainly wherever I claim feeding: this body as registered cannot reach food on flat ground with the neck held, so feeding is shown on a raised surface. The pedestal top sits 0.33 mm above the ground, and the disc centre sits 0.6 mm in front of where the mouth tip rests.

## How the fly reaches the food

Nobody told it to reach for food, and there is no line in the project that says "if sugar, reach." What happens is a chain, and each link is simple on its own.

First, the taste goes in. When the fly's mouth is on the sugar, I drive its sugar tasting neurons at 200 pulses a second. That is the only input. Think of it as the tongue tasting something sweet.

Second, the signal travels through the real wiring. Those taste neurons are connected, through the actual wiring map of a fruit fly's central brain, to other neurons, and eventually to MN9, the motor neurons that move the mouthparts in a real fly. Nothing tells MN9 to fire. It fires because the signal reaches it through the connections. That part is not programmed by me. It is computed by the wiring itself.

Third, the firing becomes movement. I read how fast MN9 is firing and translate that number into a movement: faster firing means more extension. This translator is the part I did build. It does not decide anything. It just converts a firing rate into a joint angle, the way a volume knob converts a turn into loudness.

Fourth, touch keeps it going. When the mouth touches the food, that contact switches the sugar signal back on for the next moment, so the loop feeds itself. That is why the closed loop holds on after the scripted start ends, while the open loop, which has no such feedback, lets go. The taste feedback is constructed: the model has no real taste sensors, so contact is read from the physics and fed back as a drive signal, and it is labelled constructed everywhere it appears.

## What I built, and what the wiring does

I built the translator from firing rate to extension, the taste feedback rule, the stimulus, and the arena. I did not build the brain's answers. The fact that MN9 fires on sugar, and that adding bitter crushes its firing to about an eighth, came out of the wiring, not out of any rule I wrote. Nothing anywhere in the project tells the model to suppress on bitter. The wiring did that.

The bitter test is the cleanest proof of the split. In the brain only rung, with bitter added to sugar, the feeding motor neurons' answer fell to a ratio of 0.126 of the sugar only answer, with a 95 percent interval of 0.115 to 0.138. Bitter alone left MN9 exactly silent at 0.00 Hz on both sides. And in the full loop, the sugar plus bitter arm reached only a little, with a peak extension of 0.344 rad, and never made contact in any of its twenty episodes. The suppression lives in the neural readout, which is where the registered endpoint sits.

## What one episode shows

Seed 5111 of the closed loop sugar arm is the episode in the pictures. It settled at rest, reached the food at chunk 3 with a contact force of 8.28 N, held contact while the taste event stayed on through chunk 30, then released: the event switched off at the end of chunk 31, the extension decayed, and it reached its offset at chunk 41 and stayed at zero to the end. Its peak extension was 1.969 rad at chunk 17. Across the whole arm, contact happened in all twenty episodes and the loop sustained itself through the taste gate after the scripted ignition window closed.

Seed 5111 also shows a weakness I recorded honestly: a brief interruption of about a third of a second switched the closed loop off and it never restarted, while the open loop rode through the same interruption because its drive does not depend on contact. Two of the twenty intact closed loop episodes released before the end, so any later comparison that uses persistence or duration starts from a baseline that already drops out at that rate.

## What Part 7 will test

Part 7 switches off parts of the wiring (lesions) and runs the same loop. If the reaching changes or stops when a part is switched off, then the reaching really was coming from the wiring. If nothing changes, then it was my translator doing the work all along. Each lesion is read against five matched control lesions, so a change has to beat what any similar sized switch off would do. That is the experiment the whole build exists for, and it is my finish line.

## Why I am still running it on my own laptop

A video file sent by someone else is not believable proof any more, because so much can now be generated. So I will also run this part on my own laptop, live, and record it myself showing my terminal and my IDE, for my personal YouTube. The recording pack is on GitHub at run_recording_demo.py and docs/laptop_recording_guide.md. The pictures in this project are for looking at. The laptop run is the checkable thing.
