# Debug Session: assemble-drag-errors
- **Status**: [OPEN]
- **Issue**: The assembly game opens with missing content, rejects parts with rotation errors, hides many part previews, and uses a central drop target instead of direct free-canvas placement with end-of-step validation.
- **Debug Server**: http://127.0.0.1:7777/event
- **Log File**: `.dbg/trae-debug-log-assemble-drag-errors.ndjson`

## Reproduction Steps
1. Open `/assemble/31028-sailboat`.
2. Wait for the model and current step to load.
3. Inspect the central canvas and right-side material list.
4. Drag current-step materials toward the central canvas.
5. Observe visibility, preview, rotation errors, decrement behavior, and step advancement.

## Hypotheses & Verification
| ID | Hypothesis | Likelihood | Effort | Expected Signal |
|----|------------|------------|--------|-----------------|
| A | LDraw transforms are reduced to an invalid yaw requirement | High | Low | A matching part is rejected only because calculated quarter-turn differs |
| B | Active parts are hidden and the overlay does not represent a real canvas location | High | Low | Scene state reports hidden active IDs while drop events contain no model-space point |
| C | Material cards render generic swatches instead of real part geometry | High | Low | Material payload has identifiers but no part preview scene or image |
| D | Step completion checks count only, not the exact final step state | Medium | Low | Completion fires when placed count equals expected count without a complete audit |
| E | Drag payload lacks placement and pose data | High | Low | Payload contains only step/kind/key/turn and no target coordinates |

## Log Evidence
- Hypothesis A confirmed at log lines 9-11: payload `3666:0:1` used `turn=0`; two matching instances existed but both failed the derived 90-degree requirement, producing no accepted instance.
- Hypothesis B confirmed at log line 8 and browser snapshot: step 1 had six active instances, all six were hidden, and the scene reported `visibleInstances=0`.
- Hypothesis C confirmed at log line 7 plus DOM evidence: every material group resolved to real manifest instances, but every card contained zero canvas and zero image elements.
- Hypothesis D confirmed at log lines 183-185: `finishStep` received expected and placed IDs and immediately changed to the next preview step; no independent audit result was produced.
- Hypothesis E confirmed at log line 9: the payload explicitly recorded `hasPlacementPoint=false`, and the only drop handler was the central overlay.

### Post-fix comparison
- Line 4: step 1 now reports `hiddenCount=0` and `ghostCount=6`; the browser scene reports all six instances visible and framed.
- Line 5: all three material groups report `hasPreview=true`; the browser pixel check confirms every real-geometry canvas is nonblank.
- Browser evidence confirms selecting a material creates one mouse-following real-geometry preview and disables camera orbit until placement.
- Line 35: six deliberately misplaced parts produce `audit.ok=false` with all six IDs in `wrongPositionIds`; all are returned to the material tray.
- Line 78: the same six parts placed on their instruction targets produce `audit.ok=true` with empty missing, unexpected, wrong-position, and wrong-orientation lists.
- The accepted placement record contains the actual chosen world-space position and relative quarter-turn, and survives save/reload.
- Automated verification: 56 unit tests and 51 Desktop Chrome tests pass. Coverage includes every assembly step in all 15 catalog models, a deliberately wrong six-part layout, a complete seven-step sailboat build, save/reload of manual positions, and a 121-brick subassembly placement.

## Verification Conclusion
All five hypotheses were confirmed. Post-fix evidence shows the model remains visible through ghost targets, real source-part thumbnails and a freely orbitable inspector render, the selected part follows the pointer, manual position/turn are persisted, quantities decrement, and every step passes an explicit exact-instance/position/orientation audit before advancement.
