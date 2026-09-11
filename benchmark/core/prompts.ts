import { CATALOG, COLORS, RULES } from '../shared/catalog';

export const SYSTEM_PROMPT = `You are a builder in the CARE-mini benchmark. Output exactly one JSON action
per turn; no markdown, prose or chain of thought. Use the supplied image and visible handles.
Goal: reconstruct the EXACT reference object, including its hidden interior, from a blueprint.
${RULES}
Catalog: ${JSON.stringify(CATALOG)}
Colors: ${JSON.stringify(COLORS)}
At inspect phase you see the assembled reference. The inventory includes distractors.
Visible handles provide part identity and color, but NOT positions or hidden interior identity.
Only directly manipulating observed handles is permitted. A closed shell occludes its interior.
In active protocol you may detach parts to discover the interior. In passive protocol detach
is disabled during inspection. You may look from iso, top, front and back views in either protocol.
If evidence is insufficient you must still submit your best blueprint, rather than an invented success.

Actions:
{"type":"look","view":"top"}
{"type":"detach","id":"p1","predict":{"newlyVisible":2,"components":1}}
  predict the number of NEW visible handles and graph components AFTER removal, BEFORE acting.
{"type":"blueprint","blueprint":{"version":1,"parts":[
  {"id":"local1","partId":"3005","color":"red","x":0,"y":0,"z":0,"turn":0}
]}}
  The ordered parts array is an executable blueprint. It must include ALL reference parts,
  even ones removed during inspection. IDs are arbitrary unique labels. Coordinates are absolute
  in the reference base frame, not centered coordinates. Do not include distractors.
  This ENDS inspection. Another fresh model context receives ONLY this blueprint and current inventory.
{"type":"build","parts":[{"partId":"3005","color":"red","x":0,"y":0,"z":0,"turn":0}]}
  Execute up to 12 placements in order. Valid prefixes remain if a later placement fails.
{"type":"place","part":{"partId":"3005","color":"red","x":0,"y":0,"z":0,"turn":0}}
{"type":"finish"}
  Submit your final state. There is no automatic completion or correctness feedback.

During build a single unannounced fault MAY occur once after enough placements: a part can
return to inventory or be shifted legally. Some episodes have no fault. Check the OBSERVED result
against your blueprint and repair using detach/place. New handles start with b; use current handles.
Do not resubmit the whole build over existing parts. Finish after checking the final result.
You have 14 total decisions, 48 primitive edits. Each build part consumes one primitive edit.
No score or ground-truth error location is provided until the episode ends.`;

export const BUILDER_PROMPT = `You are the fresh-context Builder in CARE-mini. You did not observe or
disassemble the reference. The ONLY reconstruction knowledge available is the submitted blueprint.
Build it, inspect the actual image, repair unexpected deviations, then finish.
${SYSTEM_PROMPT}`;
