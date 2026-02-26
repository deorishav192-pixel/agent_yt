from __future__ import annotations

import subprocess
import textwrap
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GeneratedVideo:
    video_path: Path
    description: str


class VideoGenerator:
    def __init__(self, ffmpeg_bin: str = "ffmpeg") -> None:
        self.ffmpeg_bin = ffmpeg_bin

    def generate(self, *, title: str, body: str, output_dir: Path) -> GeneratedVideo:
        output_dir.mkdir(parents=True, exist_ok=True)
        safe_stem = "".join(ch.lower() if ch.isalnum() else "-" for ch in title).strip("-") or "video"
        video_path = output_dir / f"{safe_stem}.mp4"

        wrapped = "\\n".join(textwrap.wrap(body, width=40))[:1200]
        text = f"{title}\\n\\n{wrapped}".replace(":", "\\:").replace("'", "\\'")

        cmd = [
            self.ffmpeg_bin,
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=0x1f2937:s=1280x720:d=20",
            "-vf",
            (
                "drawtext=fontcolor=white:fontsize=40:"
                "x=(w-text_w)/2:y=(h-text_h)/2:"
                f"text='{text}'"
            ),
            "-pix_fmt",
            "yuv420p",
            str(video_path),
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return GeneratedVideo(video_path=video_path, description=body[:4900])
