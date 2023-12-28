# Use a base image with Python and necessary dependencies
FROM python:3.11-slim-bookworm

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
  ffmpeg \
  libsm6 \
  libxext6 \
  libxrender-dev

# Set working directory
WORKDIR /app

# Copy project metadata files and source files
COPY pyproject.toml poetry.lock ./
COPY golden_frame ./golden_frame

# Install Poetry and project dependencies
RUN pip install poetry

# https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0
ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=1 \
  POETRY_VIRTUALENVS_CREATE=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache

RUN poetry config virtualenvs.create false
RUN poetry install && rm -rf $POETRY_CACHE_DIR

# # Install system package dependencies for OpenCV
# RUN poetry run apt-get update && apt-get install -y \
#   libopencv-dev

# Set entry point (adjust accordingly)
EXPOSE 3131
CMD ["poetry", "run", "python", "-u", "golden_frame/server.py"]
