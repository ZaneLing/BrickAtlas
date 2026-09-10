# Assembly Game

`/assemble` is the manual building mode. It is separate from the automatic
animation at `/build/:modelId`.

## Flow

1. Choose one of the 15 catalog models, ordered from difficulty 1 to 5.
2. The game loads the same verified LDraw manifest and batched geometry used by
   Explore and Build.
3. The current step remains visible as blue ghost targets.
4. Each material card renders the real source-part triangle geometry rather
   than a generic icon.
5. Selecting a material opens a freely orbitable 3D inspector. The selected
   part then follows the pointer over a target-height placement plane.
6. Click the canvas or drag from the tray to choose the part's position.
   Quarter-turn controls change its installed orientation.
7. The manual position and orientation are retained in the canvas and local
   save data. Invalid or future-step material types are rejected.
8. Material quantities decrement after every accepted part, and exhausted
   cards disappear from the current-step tray.
9. Before advancing, an explicit audit checks the exact instance set and every
   authored target position and orientation. Incorrect parts are returned to
   the material tray; placement steps audit one completed subassembly.
10. Progress is saved locally after every accepted placement and by the explicit
   Save command.
11. Completing the final step records a durable completion flag. The home model
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
