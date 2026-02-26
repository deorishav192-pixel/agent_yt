FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY yt_agent ./yt_agent
COPY instructions.yaml .

RUN pip install --no-cache-dir -e .

CMD ["python", "-m", "yt_agent.main", "--dry-run"]
