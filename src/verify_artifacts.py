from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def check_run(run_id: str) -> dict:
    d = ROOT / "artifacts" / run_id
    image_path = d / "result.png"
    manifest_path = d / "manifest.json"

    if not image_path.exists():
        raise FileNotFoundError(image_path)
    if not manifest_path.exists():
        raise FileNotFoundError(manifest_path)

    with Image.open(image_path) as im:
        size = im.size
        mode = im.mode

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256(image_path)

    return {
        "run_id": run_id,
        "size": size,
        "mode": mode,
        "bytes": image_path.stat().st_size,
        "sha256_actual": digest,
        "sha256_manifest": manifest.get("sha256"),
        "sha256_ok": digest == manifest.get("sha256"),
        "json_valid": True,
    }


def main() -> None:
    a = check_run("run_001")
    b = check_run("run_002")

    print(json.dumps({"run_001": a, "run_002": b}, indent=2, ensure_ascii=False))
    print("\nBYTEWISE SHA-256 MATCH:", a["sha256_actual"] == b["sha256_actual"])


if __name__ == "__main__":
    main()
