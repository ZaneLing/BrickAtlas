# Free DIY Studio

## Scope

`/diy` is a separate, desktop-only workspace for direct brick placement. It does not replace `/compose`, `/create`, `/explore` or `/build`.

- Right-side library: 78 traceable Part IDs, 18 colors and 12 multi-brick recipes, including furniture, street objects, plants and small structures.
- Ten searchable categories: basic bricks, plates, tiles/grilles, slopes/curves, round parts, modified bricks, Technic, connectors, architecture and motion parts.
- Pointer-following translucent preview and footprint outline, using the same geometry as placed bricks and library thumbnails.
- Click to place repeatedly; dragging or right-dragging manipulates the camera without committing a brick.
- Ninety-degree rotation and automatic stacking on existing brick tops; optional explicit plate layer.
- Paint existing bricks, select/focus/pick style, erase, undo and redo.
- Whole recipe placement is one undo action. Clear/import replacement requires confirmation and remains undoable.
- Local autosave and explicit save; storage errors remain visible without disabling the editor.
- JSON import/export, BOM CSV, LDraw, and PNG. The virtual ground is not included in the BOM or LDraw.

## Placement Coordinates

X/Z identify integer stud cells; Y identifies plate layers. One stud is 8 mm (20 LDU), and a layer is 3.2 mm (8 LDU). Rotation transforms each recipe's bounds, then normalizes it to the cursor anchor.

A sparse column index checks occupied vertical intervals. A brick above ground needs at least one supporting top stud. Tiles do not offer top attachment points, and slopes offer only their high row. Deleting a brick is rejected if the remaining scene would contain unsupported bricks. This is a conservative occupancy/support model, not a strength, balance or full mechanical connection solver.

## Rendering and Performance

- Three.js `InstancedMesh` batches by part shape and carries per-instance colors; color changes do not multiply batches.
- Part geometry is cached and reused by committed instances and the preview.
- GPU capacity grows geometrically rather than reallocating on every addition.
- CPU broad-phase ray/box tests limit exact triangle picking to candidate bricks.
- The preview updates independently of committed geometry and does not save history on pointer movement.
- The ground uses a procedural grid and a fixed 6,400-stud patch that follows the camera. Edge studs blend into the grid.
- DPR is capped by GPU texture/viewport limits and a 12-million-pixel drawing budget.
- Library thumbnails are generated with one temporary renderer, then retained in 2D canvases.

## Limits

The baseplate has no fixed scene boundary, but browser resources and floating-point precision are finite. The current cap is 5,000 bricks, 50 undo snapshots, X/Z within +/-1,000,000 stud cells and Y within 0-3,000 plate layers. Normal nearby editing is the target; precision at coordinate extremes is not certified. The maximum zoom-out distance is 200 stud units; distant work remains accessible by panning.

Procedural parts are recognizable editable representations, not full LDraw underside/tube meshes. Technic holes, clips, arches, fences, bars, wheels, dishes and propellers use category-specific procedural geometry, while collision still uses conservative stud-cell volumes. Every listed ID is checked against the repository's locked LDraw library. DIY assemblies are small prebuilt recipes, not full OMR catalog models. Exported LDraw references require a standard parts library.

## Verification

- Unit tests cover library uniqueness and locked-file existence, category population, rotations, negative/distant coordinates, occupied cells, top stacking, unsupported placements, smooth/slope/jumper attachment restrictions, all recipe rotations, protected deletion, undo/redo, malformed imports, geometry validity and LDraw coordinate conversion.
- Chrome mouse tests cover cursor preview movement, rotated stamping, stacking, recoloring, history, no placement during drag, collision rejection, atomic recipes, extended-ground placement, save/reload and file export/import.
- A 2,500-brick fixture validates shape batching and retained editing under simulated storage quota failure.
- Screenshots, nonblank pixel checks and thumbnail checks at 1180, 1440 and 3840 px desktop widths, plus axe WCAG 2 A/AA.
- Library cards use their real procedural geometry. Selecting a card can use a full-card brick shatter, normal commands use a lighter stud burst, and successful canvas placement emits a color-matched lock ring. Reduced-motion preferences disable these effects.
- Tests live in `tests/unit/diy.test.ts` and `tests/e2e/diy.spec.ts`. Measurements and screenshots are attached to the Playwright report; draw-call time is CPU submission, not GPU timer-query duration.
