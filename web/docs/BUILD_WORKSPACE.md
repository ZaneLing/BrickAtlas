# Build Workspace

The central 3D model is the only animated assembly surface. Restart, previous, next, slider, play and pause update the model without opening or changing any guide accordion. Optional camera follow controls only the central camera.

The right guide is deliberately static and user-controlled:

- Every step starts collapsed, including after reload.
- Opening a step selects that step in the central model and closes the previously opened guide block.
- Step navigation does not alter the open block.
- A step contains its grouped, clickable parts and one 2560x1120 PNG rendered from the exact source geometry.
- The PNG combines a focused start frame and final installation frame with an explicit arrow.
- Clicking the diagram opens a wide resolution-preserving preview.
- Clicking a part opens its interactive 3D part preview, part number, color, quantity and dimensions.

Both sidebars collapse independently. The CSS grid removes the hidden track, so the center receives the released width rather than covering it with an overlay. Reopen buttons remain on the corresponding canvas edge.

The static guide captures use a separate renderer and restore all live scene state, camera, environment, visibility data and assembly progress. Generation starts only for a manually opened step and is cancelled when that block or the right guide closes.
