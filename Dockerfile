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
RUN poetry install --no-interaction --no-ansi --only main

# Copy full application
COPY . /app/

ENV PYTHONPATH="/app/services/ese-core"

# Default entrypoint (will be overridden in docker-compose.ese.yml)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
