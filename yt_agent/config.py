from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class UploadDefaults:
    category_id: str = "22"
    privacy_status: str = "private"
    made_for_kids: bool = False


@dataclass
class AgentSettings:
    instruction_file: Path = Path("instructions.yaml")
    output_dir: Path = Path("build")
    poll_interval_seconds: int = 300
    ffmpeg_bin: str = "ffmpeg"
    youtube_client_secret_file: Path = Path("secrets/client_secret.json")
    youtube_token_file: Path = Path("secrets/token.json")
    defaults: UploadDefaults = field(default_factory=UploadDefaults)

    @classmethod
    def from_env(cls) -> "AgentSettings":
        return cls(
            instruction_file=Path(os.getenv("YT_AGENT_INSTRUCTION_FILE", "instructions.yaml")),
            output_dir=Path(os.getenv("YT_AGENT_OUTPUT_DIR", "build")),
            poll_interval_seconds=int(os.getenv("YT_AGENT_POLL_INTERVAL_SECONDS", "300")),
            ffmpeg_bin=os.getenv("YT_AGENT_FFMPEG_BIN", "ffmpeg"),
            youtube_client_secret_file=Path(
                os.getenv("YT_AGENT_YOUTUBE_CLIENT_SECRET_FILE", "secrets/client_secret.json")
            ),
            youtube_token_file=Path(os.getenv("YT_AGENT_YOUTUBE_TOKEN_FILE", "secrets/token.json")),
        )
