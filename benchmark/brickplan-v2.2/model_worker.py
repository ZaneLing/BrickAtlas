"""One isolated, real MLX-VLM inference. JSON stdin/stdout; no benchmark imports."""
import contextlib
import json
import sys


def main():
    request = json.load(sys.stdin)
    with contextlib.redirect_stdout(sys.stderr):
        import mlx.core as mx
        from mlx_vlm import load, generate
        from mlx_vlm.prompt_utils import apply_chat_template
        mx.random.seed(0)
        model, processor = load(request["modelPath"])
        # Explicit, reproducible model-side downsampling; stored stimuli remain HD.
        processor.image_processor.size = {"longest_edge": 512}
        processor.image_processor.do_image_splitting = False
        formatted = apply_chat_template(processor, model.config, request["prompt"],
                                        num_images=len(request["images"]))
        result = generate(model, processor, formatted, image=request["images"],
                          max_tokens=request["maxTokens"], temperature=0, verbose=False)
    print(json.dumps({"rawOutput": result.text, "formattedPrompt": formatted,
                      "usage": {"inputTokens": result.prompt_tokens, "outputTokens": result.generation_tokens,
                                "costUSD": 0, "source": "mlx_vlm.GenerationResult"},
                      "preprocessing": {"longestEdge": 512, "imageSplitting": False}}))


if __name__ == "__main__":
    main()
