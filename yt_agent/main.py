from __future__ import annotations

import argparse
import logging
import time

from yt_agent.agent import YouTubeAutomationAgent
from yt_agent.config import AgentSettings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YouTube content automation agent")
    parser.add_argument("--daemon", action="store_true", help="Keep polling instruction file")
    parser.add_argument("--dry-run", action="store_true", help="Generate videos without uploading")
    parser.add_argument("--log-level", default="INFO")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    logging.basicConfig(level=args.log_level.upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    settings = AgentSettings.from_env()
    agent = YouTubeAutomationAgent(settings)

    if not args.daemon:
        agent.run_once(dry_run=args.dry_run)
        return 0

    while True:
        try:
            agent.run_once(dry_run=args.dry_run)
        except Exception:
            logging.exception("Agent loop iteration failed")
        time.sleep(settings.poll_interval_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
