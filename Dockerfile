# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for pedalboard and audio processing
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Install pedalboard and any other dependencies
RUN pip install --no-cache-dir pedalboard numpy scipy soundfile librosa

# Copy the project files into the container
COPY . /code_backup_from_buildtime

# Set the command to run the audio processing script
CMD ["python", "app.py"]



# to run it, do:
#   docker build -t post-process-audio .
#   docker run -d -it --gpus=all --name AudioPostProcess -v "c:\path\to\code:/app" post-process-audio /bin/bash
#