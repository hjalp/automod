# Use an official Python runtime as the base image
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the contents of the src directory to the working directory in the container
COPY src/ .

# Copy config.yaml into the config folder
COPY config.yaml ./config

# Set the entry point for the container
ENTRYPOINT [ "python", "main.py" ]
