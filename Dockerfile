FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libimage-exiftool-perl \
    clang \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/
RUN pip install --no-cache-dir -e . || true

ENTRYPOINT ["python3", "-m", "livephoto.cli"]
CMD ["--help"]
