# Lost and Found

A 62-second single static shot, made by Seal. A train-station lost-and-found shelf at night. An old umbrella stands among the forgotten things. Each time the far door opens, it leans a few degrees toward the door, then settles. The last time, the door opens and nobody comes in, and the umbrella stays leaning.

Watch: https://renders.heyseal.ai/deliverables/3af6dff4-961b-47d5-840c-77eaf506f998/ab3c33b1-fac8-489b-beaa-e2742ae775c5.mp4

## How it's made

Everything is code. No image or video model.

- `timeline.py` holds the one timeline that picture and sound both read: the door angle, the umbrella's angle and the passers-by, all as functions of time.
- `render.py` draws each 1920x1080 frame in numpy and PIL: the shelf plate, a rotating umbrella layer pinned at its tip, the door with its cold light spill and cast shadows, then grain and tone. `python3 render.py film out.mp4 8 LO HI` renders a frame range, so the film was split across two 8-core rented machines.
- `sound.py` synthesizes the soundtrack: room tone, fluorescent hum, distant trains, the door latch and swing, and a sparse low tone.
- The halves were joined and muxed with ffmpeg.

## Versions

- v1: first plate and timeline. The umbrella leaned away from the door, and against the dark shelf upright it was barely readable.
- v2: the lean was reversed toward the door and made larger, the umbrella got a contact shadow, and the door swung wider at the end. The rabbit's smile was flattened.
- v3/v4: a rim light on the handle and a stronger lean. The reviewer still read it as sliding, not tipping.
- v5: the umbrella moved about 77px off the shelf post, starts near vertical (1.5°) and pivots at a fixed tip, building to about 10.8° toward the door.
- v6: a wider umbrella layer, so the canopy no longer clips when it rotates. First full render. The reviewer said the back half went flat: 50s and 61s looked like one pose.
- v7 (this cut): each opening pushes the lean further, about 4.5°, 9° and 14°, then a creep to about 17° on the final hold. Measuring the frames confirmed the tip stays pinned at x≈914 and the door spill is present on the last opening, so a later reviewer note about sliding was wrong and was set aside.

Each pass was reviewed by Claude Opus looking at the frames. That loop caught the wrong-direction lean, the slide-not-tip read and the canopy clipping.
