# YouTube Video Agent

An autonomous Python agent that:
1. reads your content instructions,
2. generates a short video asset,
3. uploads it to your YouTube channel using YouTube Data API.

## What this gives you
- **Instruction-driven workflow**: you control topics, script text, tags, and privacy in `instructions.yaml`.
- **Reliable execution**: retries on generation failures and logs each stage.
- **Safe rollout path**: `--dry-run` mode to stabilize before enabling uploads.
- **Deployable service**: Docker image + GitHub Actions deploy workflow skeleton.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Set up Google API credentials:
- Enable **YouTube Data API v3** in Google Cloud.
- Create OAuth client credentials (Desktop app).
- Save JSON to `secrets/client_secret.json`.

Run first in dry-run mode:

```bash
python -m yt_agent.main --dry-run
```

Then run live upload mode:

```bash
python -m yt_agent.main
```

Daemon mode for continuous automation:

```bash
python -m yt_agent.main --daemon
```

## Deployment

### Docker
```bash
docker build -t youtube-agent:latest .
docker run --rm \
  -v $(pwd)/instructions.yaml:/app/instructions.yaml \
  -v $(pwd)/secrets:/app/secrets \
  --env-file .env \
  youtube-agent:latest python -m yt_agent.main --daemon
```

### GitHub Actions deploy
A sample workflow is in `.github/workflows/deploy.yml`.
It deploys over SSH after tests pass. Configure repository secrets:
- `SSH_PRIVATE_KEY`
- `DEPLOY_HOST`
- `DEPLOY_USER`
- `DEPLOY_PATH`

## Stability checklist before full autopost
- Validate at least 5 runs with `--dry-run`.
- Validate 2 successful private uploads.
- Confirm title/description/tag quality in YouTube Studio.
- Switch `privacy_status` to `public` only after quality checks.
