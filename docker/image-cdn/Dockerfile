# Docker to serve Flask via Unicorn
FROM ubuntu:22.04

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Configure our networking to point to the Redis instance included in docker compose
ENV REDIS_HOST=redis

# Install tools and additional dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        dos2unix \
        python3-pip python3-dev \
        gcc netcat curl cron libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the contents of `image-cdn` (except for any images already on the host machine)
COPY image-cdn/requirements.txt /image-cdn/
COPY image-cdn/server.py /image-cdn/
COPY image-cdn/worker.py /image-cdn/
WORKDIR /image-cdn

# Install requirements
RUN pip3 install gunicorn wheel
RUN pip3 install -r requirements.txt
