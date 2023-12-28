# ? OpenCV Dependencies, probably needed in all images
FROM python:3.11-slim-bookworm as base

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
  ffmpeg \
  libsm6 \
  libxext6 \
  libxrender-dev

# ? Builder
FROM base as builder

# Install Poetry and project dependencies
# https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0
RUN pip install poetry
ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=1 \
  POETRY_VIRTUALENVS_CREATE=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Copy source files
COPY pyproject.toml poetry.lock ./
COPY golden_frame ./golden_frame

RUN poetry install && rm -rf $POETRY_CACHE_DIR

# ? Runner
FROM base as runner

USER nobody
WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
  PATH="/app/.venv/bin:$PATH"

COPY --from=builder --chown=nobody:nobody ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY --chown=nobody:nobody golden_frame ./golden_frame

EXPOSE 3131
CMD ["python", "-u", "golden_frame/server.py"]
