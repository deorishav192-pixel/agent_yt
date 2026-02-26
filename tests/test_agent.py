from pathlib import Path

from yt_agent.agent import YouTubeAutomationAgent
from yt_agent.config import AgentSettings


class DummyGenerator:
    def generate(self, *, title: str, body: str, output_dir: Path):
        output_dir.mkdir(exist_ok=True)
        p = output_dir / "dummy.mp4"
        p.write_text("video")
        return type("G", (), {"video_path": p, "description": body})


class DummyPublisher:
    def upload(self, **kwargs):
        return {"id": "abc123"}


def test_run_once_dry_run(tmp_path: Path) -> None:
    instruction_file = tmp_path / "instructions.yaml"
    instruction_file.write_text(
        '{"queue":[{"title":"A","body":"B"}]}'
    )
    settings = AgentSettings(
        instruction_file=instruction_file,
        output_dir=tmp_path / "build",
        youtube_client_secret_file=tmp_path / "secret.json",
        youtube_token_file=tmp_path / "token.json",
    )
    agent = YouTubeAutomationAgent(settings)
    agent.generator = DummyGenerator()
    agent.publisher = DummyPublisher()

    out = agent.run_once(dry_run=True)
    assert len(out) == 1
    assert out[0].exists()
