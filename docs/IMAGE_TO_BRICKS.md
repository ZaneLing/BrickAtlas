# Image-to-Bricks Pipeline

## Browser Reconstruction

`/create` starts empty and converts the user's own real-object photographs. It no longer shows a fixed vehicle demo.

The local pipeline:

1. accepts one required front photograph and optional left, back, and right photographs;
2. preserves the complete image by default, with manual square cropping still available;
3. runs the Apache-2.0 Depth Anything V2 Small ONNX model in a Web Worker;
4. estimates and flood-fills the connected background while preserving transparent image masks;
5. converts single-image depth into a smoothed 3D surface shell instead of a flat color relief;
6. intersects aligned silhouettes when two to four views are supplied;
7. supports hollow, solid, and low-profile relief output;
8. quantizes colors in CIELAB space against the supported LDraw palette;
9. packs voxels into 1x1 through 1x4 and 2x2 through 2x4 bricks;
10. reduces resolution automatically to stay within the requested brick budget;
11. creates stable brick IDs, bottom-up build steps, BOM data, and LDraw output; and
12. renders the result with batched Three.js instancing.

The depth model is downloaded once from the
[ONNX community Depth Anything V2 Small repository](https://huggingface.co/onnx-community/depth-anything-v2-small)
and is then handled by the browser cache. The URL is pinned to revision
`4472b7362082ad9968fee890ca0f1e5aca36b93d`, and the worker verifies the model's SHA-256 before inference. Photos stay in the browser. If model loading is unavailable, the generator falls back to deterministic silhouette-distance reconstruction.

## Why a Single Image Is Not Enough for Exact Geometry

A photograph contains no direct evidence for the back, underside, internal supports, real scale, or occluded parts of an object. Monocular depth supplies a plausible visible surface, not ground-truth hidden geometry. For better reconstruction, photograph the same stationary object from front, left, back, and right at a similar distance and height.

BrickLink Studio makes the same practical distinction:

- image files are imported as mosaics;
- OBJ or STL meshes are imported as 3D sculptures.

References:

- [BrickLink Studio Mosaic](https://studiohelp.bricklink.com/hc/en-us/articles/5625025298327-Mosaic)
- [BrickLink Studio import formats](https://studiohelp.bricklink.com/hc/en-us/articles/6502277722647-Import-formats)
- [Image2Lego paper](https://arxiv.org/abs/2108.08477)

## Optional Cloud Reconstruction

For higher-fidelity production reconstruction:

1. Validate and normalize the upload.
2. Segment the subject and remove the background.
3. Run a dedicated image-to-3D model.
4. repair and normalize the generated mesh;
5. voxelize the watertight volume at the requested stud resolution;
6. pack voxels into an allowed brick catalog with alternating seams;
7. verify support, connectivity, collisions, and center of mass;
8. generate LDraw, BOM, and bottom-up build steps; and
9. send the result to the existing Brick Atlas viewer.

Candidate reconstruction backends:

- Alibaba Cloud Model Studio Tripo supports single-image and ordered front/left/back/right multi-image GLB generation. It is the closest match for this workflow, but requires the Tripo product to be enabled for the Beijing-region key.
- [TripoSR](https://github.com/VAST-AI-Research/TripoSR) is an MIT-licensed self-hosted alternative and needs substantially more compute than the browser path.
- OpenRouter image models generate or edit raster images; they do not return a reliable watertight 3D mesh and are therefore not used as the geometry source.

Open implementations such as [Bricked](https://github.com/evanesmiller/Bricked) and [BrickBuilder](https://github.com/jjohnson5253/brickbuilderai) use the same broad sequence: segmentation, reconstruction, voxelization, brick packing, and Three.js visualization.

## Suggested Service Contract

Any cloud integration must upload images through a private job API rather than expose a provider key:

```text
POST /api/image-builds
GET  /api/image-builds/:id
GET  /api/image-builds/:id/model.ldr
GET  /api/image-builds/:id/bom.csv
```

The result should use stable brick IDs and include:

```json
{
  "version": 1,
  "source": {
    "views": 1,
    "reconstructionModel": "triposr",
    "modelVersion": "pinned-version"
  },
  "bricks": [],
  "steps": [],
  "bom": [],
  "validation": {
    "connected": false,
    "supported": false,
    "physicallyVerified": false
  }
}
```

Generated geometry must remain labeled as inferred until connectivity and physical build checks pass.
