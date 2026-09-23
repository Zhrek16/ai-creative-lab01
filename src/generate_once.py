from __future__ import annotations

import argparse
import hashlib
import importlib.metadata as metadata
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import torch
from diffusers import AutoPipelineForText2Image
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "configs" / "run_config.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def package_version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "not-installed"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="run_001")
    args = parser.parse_args()

    cfg = load_config()
    out = ROOT / "artifacts" / args.run_id
    out.mkdir(parents=True, exist_ok=True)

    if cfg["device"] != "cpu":
        raise ValueError("This lab configuration is intentionally fixed to CPU.")

    torch.set_num_threads(int(cfg.get("torch_num_threads", 1)))
    torch.use_deterministic_algorithms(
        bool(cfg.get("deterministic_algorithms", True))
    )

    dtype = torch.float32
    generator = torch.Generator(device="cpu").manual_seed(int(cfg["seed"]))

    print("=== Reproducible text-to-image run ===")
    print("Python:", sys.version.replace("\n", " "))
    print("Platform:", platform.platform())
    print("PyTorch:", torch.__version__)
    print("Diffusers:", package_version("diffusers"))
    print("Transformers:", package_version("transformers"))
    print("Accelerate:", package_version("accelerate"))
    print("Safetensors:", package_version("safetensors"))
    print("CUDA available:", torch.cuda.is_available())
    print("Model:", cfg["model_id"])
    print("Revision:", cfg["revision"])
    print("Seed:", cfg["seed"])
    print("Steps:", cfg["num_inference_steps"])
    print("Guidance:", cfg["guidance_scale"])
    print("Size:", f'{cfg["width"]}x{cfg["height"]}')
    print("Device:", cfg["device"])
    print("dtype:", dtype)

    print("\nLoading pipeline...")
    pipeline = AutoPipelineForText2Image.from_pretrained(
        cfg["model_id"],
        revision=cfg["revision"],
        torch_dtype=dtype,
    )
    pipeline = pipeline.to(cfg["device"])
    pipeline.set_progress_bar_config(disable=True)

    print("Generating...")
    start = time.perf_counter()
    result = pipeline(
        prompt=cfg["prompt"],
        num_inference_steps=int(cfg["num_inference_steps"]),
        guidance_scale=float(cfg["guidance_scale"]),
        height=int(cfg["height"]),
        width=int(cfg["width"]),
        generator=generator,
    )
    elapsed = time.perf_counter() - start

    image = result.images[0]
    if not isinstance(image, Image.Image):
        image = Image.fromarray(image)

    image_path = out / "result.png"
    image.save(image_path, format="PNG")
    digest = sha256_file(image_path)

    manifest = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "model_id": cfg["model_id"],
        "revision": cfg["revision"],
        "prompt": cfg["prompt"],
        "seed": int(cfg["seed"]),
        "steps": int(cfg["num_inference_steps"]),
        "guidance_scale": float(cfg["guidance_scale"]),
        "height": int(cfg["height"]),
        "width": int(cfg["width"]),
        "device": cfg["device"],
        "dtype": str(dtype),
        "deterministic_algorithms": bool(
            cfg.get("deterministic_algorithms", True)
        ),
        "torch_num_threads": int(cfg.get("torch_num_threads", 1)),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": {
            "torch": torch.__version__,
            "diffusers": package_version("diffusers"),
            "transformers": package_version("transformers"),
            "accelerate": package_version("accelerate"),
            "safetensors": package_version("safetensors"),
            "Pillow": package_version("Pillow"),
        },
        "elapsed_seconds_measured": round(elapsed, 3),
        "artifact": str(image_path.relative_to(ROOT)),
        "artifact_bytes": image_path.stat().st_size,
        "sha256": digest,
    }

    manifest_path = out / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\n=== RESULT ===")
    print("Image:", image_path)
    print("Size:", image.size, image.mode)
    print("Bytes:", image_path.stat().st_size)
    print("Elapsed:", round(elapsed, 3), "s")
    print("SHA-256:", digest)
    print("Manifest:", manifest_path)


if __name__ == "__main__":
    main()
