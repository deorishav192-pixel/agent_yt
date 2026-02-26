from __future__ import annotations

import logging
import time
from pathlib import Path

from yt_agent.config import AgentSettings
from yt_agent.instructions import ClipInstruction, InstructionSet, load_instruction_set
from yt_agent.video_generator import GeneratedVideo, VideoGenerator
from yt_agent.youtube_client import YouTubePublisher

logger = logging.getLogger(__name__)


class YouTubeAutomationAgent:
    def __init__(self, settings: AgentSettings) -> None:
        self.settings = settings
        self.generator = VideoGenerator(ffmpeg_bin=settings.ffmpeg_bin)
        self.publisher = YouTubePublisher(
            client_secret_file=settings.youtube_client_secret_file,
            token_file=settings.youtube_token_file,
        )

    def load_queue(self) -> InstructionSet:
        return load_instruction_set(self.settings.instruction_file)

    def _generate_video(self, clip: ClipInstruction) -> GeneratedVideo:
        last_error = None
        for attempt in range(1, 4):
            try:
                return self.generator.generate(title=clip.title, body=clip.body, output_dir=self.settings.output_dir)
            except Exception as exc:
                last_error = exc
                logger.warning("Generate attempt %s failed for %s: %s", attempt, clip.title, exc)
                time.sleep(min(2**attempt, 10))
        assert last_error is not None
        raise last_error

    def process_clip(self, clip: ClipInstruction, default_tags: list[str], dry_run: bool = False) -> Path:
        logger.info("Generating video for '%s'", clip.title)
        generated = self._generate_video(clip)
        if dry_run:
            logger.info("Dry run enabled; skipping upload for %s", generated.video_path)
            return generated.video_path

        tags = sorted(set(default_tags + clip.tags))
        response = self.publisher.upload(
            video_path=generated.video_path,
            title=clip.title,
            description=generated.description,
            tags=tags,
            category_id=self.settings.defaults.category_id,
            privacy_status=clip.privacy_status or self.settings.defaults.privacy_status,
            made_for_kids=self.settings.defaults.made_for_kids,
        )
        logger.info("Uploaded '%s' successfully. id=%s", clip.title, response.get("id"))
        return generated.video_path

    def run_once(self, dry_run: bool = False) -> list[Path]:
        instruction_set = self.load_queue()
        processed = []
        for clip in instruction_set.queue:
            processed.append(self.process_clip(clip, instruction_set.default_tags, dry_run=dry_run))
        return processed
