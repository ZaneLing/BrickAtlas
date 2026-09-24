# BrickAtlas LDraw-1 source and question policy

This release replaces the synthetic Hierarchy-3 benchmark after user review
identified disconnected imitation geometry, repeated constructors, and
ambiguous module references. The earlier nominal servo protocol did not
establish real LEGO connectivity. Its counts and scores must not be presented
as measurements on this replacement.

The user explicitly authorized original LDraw/OMR files as benchmark cases on
2026-09-17. That supersedes the earlier reference-only restriction.

## Source integrity

- Preserve original MPD bytes, authors, license, source URL and SHA256.
- Preserve the complete source geometry, transforms, colors, and hierarchy.
- Use real LDraw part geometry through the existing Three.js LDrawLoader.
- Never repair a source by moving parts, adding hidden supports, changing joint
  types, or silently substituting unavailable parts.
- Exclude unresolved dependencies, unsupported textures, missing attribution,
  duplicated placements, and failed geometry/identity conversion.
- One primary build per set family; alternative builds and small generated
  variants do not increase source count.
- Report cross-source geometry and inventory similarity. A different source ID
  alone is insufficient evidence of diversity.
- Source scene objects (a vehicle and driver, for example) may be separate.
  Do not invent edges to make a scene one connected component.

## Evidence

BrickNet 0.1.0 provides connector matching for studs, holes, axles, hinges,
balls and fixed interfaces. Its original tolerance and alias rules are
recorded. Unsupported pieces remain explicitly unsupported.

The upstream inset meshes provide intersection candidates. A friction-pin or
gear intersection is not automatically a CAD defect; report whether the pair
has a recognized mating interface. Do not claim a full physical pass from
these tests, suppress unknown parts, or change the source to improve a score.
Collision checks use the original alias-transformed source poses; connector
inference uses the upstream algorithm's documented rotation normalization,
whose maximum effect is recorded.

## References and questions

Each source instance has a stable B0001-style number, distinct from its part
type. A question must bind every operand to a number and an instance ID.
The 3D view, numbered focus/isolated view, exports, public inputs and scoring
must agree. A name or highlight color alone is not a sufficient reference.
Only relevant numbers are shown together to avoid covering the whole model.

Derive answers from actual source attributes, transformations, source STEP
metadata or identified connector evidence. Do not infer physical assembly
order from source-list order, AABB overlap, semantic names, or a fabricated
module graph. For sources without STEP, omit source-step questions.

Source-step replay represents author instructions. Connector reasoning is
explicitly about identified interfaces. Temporary question interventions do
not modify the original model or certify continuous insertion/extraction.
Unmeasured forces, passive stability, gear coupling and dynamic responses
must not be asserted as ground truth.

Public question exports exclude answers and answer-revealing attributes for
visual questions. Reference solutions are intentionally accessible only in
the review artifacts. Review decisions use a new versioned storage namespace,
preserving old human feedback unchanged.

## Reporting

Use the actual retained source and question counts; do not preserve the old
144/6,912 totals by padding. D1--D4 can describe measured source scale, but
cannot be claimed to be calibrated human or model difficulty. Report task
applicability instead of inventing the same physical task for every model.
The paper and supplement remain English and use real model renders.
