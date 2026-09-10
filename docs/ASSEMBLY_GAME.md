# Assembly Game

`/assemble` is the manual building mode. It is separate from the automatic
animation at `/build/:modelId`.

## Flow

1. Choose one of the 15 catalog models, ordered from difficulty 1 to 5.
2. The game loads the same verified LDraw manifest and batched geometry used by
   Explore and Build.
3. The current step's unplaced instances are hidden.
4. Drag a material from the guide into the central installation target.
5. Select a material and rotate it in 90-degree increments with the button or
   `R` key. The target orientation is derived from the source LDraw matrix.
6. The payload is checked against the current step, part number, color,
   quarter-turn orientation, and remaining quantity. Rotationally symmetric
   parts accept any quarter turn.
7. A valid instance is revealed and receives the existing GPU placement
   animation. Invalid or future-step material is rejected.
8. The game advances only after every required instance is placed. Placement
   steps accept one completed subassembly.
9. Progress is saved locally after every accepted placement and by the explicit
   Save command.
10. Completing the final step records a durable completion flag. The home model
   card and assembly catalog then show a completion check.

## Guide Media

Only the selected guide step is rendered. Seven 960x620 frames are captured
from the verified model geometry and loop in the right panel. The first and
last frames are also displayed as a static before/after comparison. Rendering
one step at a time bounds GPU and object-URL memory even for models with
hundreds of steps.

## Persistence

The `brick-atlas-assembly-game-v1` local-storage record stores:

- completed step count;
- instance IDs already placed in the active step;
- the accepted quarter-turn for each placed instance;
- completion status; and
- update time.

Malformed records are ignored. Reset removes only the selected model's manual
assembly progress.

## Product Boundary

Validation proves that the player selected the expected catalog instance for
the authored/editorial step. It does not simulate hand collision, clutch
strength, gravity, or physical reachability. Editorial steps remain labeled as
structural guides rather than official LEGO instructions.
