FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install --no-cache-dir poetry

# Configure poetry to not use virtualenv inside container
RUN poetry config virtualenvs.create false

# Copy dependency files
COPY pyproject.toml /app/

# Install dependencies (ignoring dev group to keep image size small)
RUN poetry install --no-interaction --no-ansi --only main --no-root

# Copy full application
COPY . /app/

ENV PYTHONPATH="/app/services/ese-core"

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 CMD python -c "import os,urllib.request; port=os.environ.get('PORT','8000'); urllib.request.urlopen(f'http://127.0.0.1:{port}/livez')"

# Default entrypoint (launches the internal service processes and the Cloud Run gateway)
CMD ["sh", "/app/start-demo-platform.sh"]
