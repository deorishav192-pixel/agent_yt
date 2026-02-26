from pathlib import Path

from yt_agent.instructions import load_instruction_set


def test_load_instruction_set(tmp_path: Path) -> None:
    file = tmp_path / "instructions.yaml"
    file.write_text('{"channel_voice":"test","queue":[{"title":"Hello","body":"World"}]}')

    data = load_instruction_set(file)
    assert data.channel_voice == "test"
    assert len(data.queue) == 1
    assert data.queue[0].title == "Hello"
