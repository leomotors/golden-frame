# Use a base image with Python and necessary dependencies
FROM python:3.11-slim-buster

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
  ffmpeg \
  libsm6 \
  libxext6 \
  libxrender-dev

# Set working directory
WORKDIR /app

# Copy project metadata files and source files
COPY pyproject.toml poetry.lock app.py ./

# Install Poetry and project dependencies
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install

# # Install system package dependencies for OpenCV
# RUN poetry run apt-get update && apt-get install -y \
#   libopencv-dev

# Set entry point (adjust accordingly)
EXPOSE 3131
CMD ["poetry", "run", "python", "-u", "app.py"]
