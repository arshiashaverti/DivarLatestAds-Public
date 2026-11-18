import json
import os
from pathlib import Path
from typing import Any


def load_ids(path: str | Path) -> set[str]:
    state_path = Path(path)

    if not state_path.exists():
        return set()

    try:
        data: Any = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            f"Could not read state file: {state_path}"
        ) from exc

    if not isinstance(data, dict) or not isinstance(data.get("ids"), list):
        raise RuntimeError(f"Invalid state file format: {state_path}")

    return {
        item for item in data["ids"]
        if isinstance(item, str) and item
    }


def save_ids(path: str | Path, ids: set[str]) -> None:
    state_path = Path(path)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    payload = json.dumps(
        {"ids": sorted(ids)},
        ensure_ascii=False,
        indent=2,
    )

    temporary = state_path.with_name(state_path.name + ".tmp")

    try:
        temporary.write_text(payload + "\n", encoding="utf-8")
        os.replace(temporary, state_path)
    finally:
        if temporary.exists():
            temporary.unlink()


def find_new_ads(
    ads: list[dict[str, str]],
    known_ids: set[str],
) -> list[dict[str, str]]:
    return [ad for ad in ads if ad["id"] not in known_ids]