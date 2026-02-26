from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ClipInstruction:
    title: str
    body: str
    tags: list[str] = field(default_factory=list)
    thumbnail_text: str | None = None
    publish_now: bool = False
    privacy_status: str = "private"


@dataclass
class InstructionSet:
    channel_voice: str = "Educational and concise"
    default_tags: list[str] = field(default_factory=list)
    queue: list[ClipInstruction] = field(default_factory=list)


def _minimal_yaml_parse(text: str) -> dict:
    """Very small parser for the included sample format when PyYAML isn't installed."""
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text) or {}
    except Exception:
        # Fallback expects JSON syntax.
        return json.loads(text)


def load_instruction_set(path: Path) -> InstructionSet:
    raw = _minimal_yaml_parse(path.read_text())
    queue = [ClipInstruction(**item) for item in raw.get("queue", [])]
    return InstructionSet(
        channel_voice=raw.get("channel_voice", "Educational and concise"),
        default_tags=raw.get("default_tags", []),
        queue=queue,
    )
