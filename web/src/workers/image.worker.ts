import { createBrickModelFromViews, type ImageBrickOptions, type ImageBrickViews } from '../creator/imageBrickModel';

self.onmessage = (event: MessageEvent<{ views: ImageBrickViews; options: ImageBrickOptions; name: string }>) => {
  try {
    const { views, options, name } = event.data;
    self.postMessage({ build: createBrickModelFromViews(views, options, name) });
  } catch (error) {
    self.postMessage({ error: error instanceof Error ? error.message : String(error) });
  }
};
