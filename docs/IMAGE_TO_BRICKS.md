# Image-to-Bricks Pipeline

## What Ships in the Browser

Brick Atlas includes a deterministic local multi-view generator at `/create`.

The browser:

1. lets the user move and resize a square crop independently on each source image;
2. accepts a required front view plus optional top and side views;
3. samples each crop onto a common configurable stud grid;
4. estimates the background from corner pixels;
5. maps visible pixels to a practical LDraw color palette;
6. derives either a shallow height field or a three-view visual hull;
7. supports solid, hollow-shell, and relief generation;
8. packs occupied cells into 1x1, 1x2, 1x3, and 1x4 bricks using stacked, running, or reinforced bonds;
9. lowers sampling resolution automatically when needed to honor the requested brick budget;
10. creates bottom-up build steps and a bill of materials;
11. renders the result with batched Three.js instancing; and
12. exports BOM CSV and LDraw files.

No image is uploaded. Multi-view output is a silhouette intersection, not a learned reconstruction of surfaces hidden from every supplied view.

## Why a Single Image Is Not Enough for Exact Geometry

A photograph contains no direct evidence for the back, underside, internal supports, real scale, or occluded parts of an object. A model can infer plausible geometry, but it cannot guarantee an exact reconstruction from one view. Exact work requires calibrated multi-view photographs or an existing mesh. The browser workflow improves silhouette and depth agreement when front, top, and side views are supplied, but it does not infer unseen concavities.

BrickLink Studio makes the same practical distinction:

- image files are imported as mosaics;
- OBJ or STL meshes are imported as 3D sculptures.

References:

- [BrickLink Studio Mosaic](https://studiohelp.bricklink.com/hc/en-us/articles/5625025298327-Mosaic)
- [BrickLink Studio import formats](https://studiohelp.bricklink.com/hc/en-us/articles/6502277722647-Import-formats)
- [Image2Lego paper](https://arxiv.org/abs/2108.08477)

## Recommended Volumetric Architecture

For a future full sculpture service:

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

- [TripoSR](https://github.com/VAST-AI-Research/TripoSR): MIT-licensed, single-image reconstruction, approximately 6 GB VRAM for its reference inference path.
- [Hunyuan3D 2.1](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1): higher-end shape and texture pipeline with a custom community license that must be reviewed for the deployment region and product.
- [Depth Anything V2](https://github.com/DepthAnything/Depth-Anything-V2): useful for depth-assisted reliefs, but a depth map alone does not recover a closed object.

Open implementations such as [Bricked](https://github.com/evanesmiller/Bricked) and [BrickBuilder](https://github.com/jjohnson5253/brickbuilderai) use the same broad sequence: segmentation, reconstruction, voxelization, brick packing, and Three.js visualization.

## Suggested Service Contract

The browser should upload images to a private job API rather than expose a model-provider key:

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
