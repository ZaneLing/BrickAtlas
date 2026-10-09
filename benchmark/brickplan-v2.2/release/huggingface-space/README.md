---
title: BrickPlan 2.2
emoji: 🧱
colorFrom: green
colorTo: gray
sdk: docker
app_port: 7860
---

# BrickPlan: visual planning questions and model feedback

377 interactive episodes, 1952 diagnostic questions and 16 source groups.
The homepage explains seven task families, previews complete questions,
and links a historical BrickPlan 2.1 SmolVLM integration case, not a new 2.2 measurement.

This prepared Space package has not been uploaded. Upload the three files
in this folder to an owner-selected Hugging Face Docker Space.
The first build installs Python dependencies and the source-triangle raster.
Model weights are not bundled. The recorded case works without any provider.

Live local MLX inference requires Apple silicon and is unavailable on a
standard Linux Space. An OpenAI-compatible model can be configured using
Space secrets `BRICKPLAN_API_KEY`, `BRICKPLAN_API_BASE` and `BRICKPLAN_MODEL`.
Use a private Space for credential-backed demonstrations: this practice
server shares one state store and is not a multi-user study or billing service.
For participant studies, use separately configured stores and gateways.

The store in this Docker example is ephemeral. A restart discards
interactive practice data; the archived case and dataset remain in the image.
Use `--store /data/brickplan-practice` when persistent Space storage is enabled.
The Docker build is a deployment recipe; local archive extraction and runtime
are verified separately from a hosted Space build.
