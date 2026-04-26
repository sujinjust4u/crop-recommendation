#!/bin/bash

# Exit on any error
set -e

# Build the Docker image
echo "Building the Docker image..."
docker build -t crop-recommendation-app .

# Stop and remove any existing container with the same name
echo "Stopping any existing container..."
docker stop crop-recommendation-container 2>/dev/null || true
docker rm crop-recommendation-container 2>/dev/null || true

# Run the Docker container
echo "Running the Docker container on port 8080..."
docker run -d -p 8080:5000 --name crop-recommendation-container -e GEMINI_API_KEY="AIzaSyA41_i64ESFdHL2oQy2VlmqnjEnWB88K3M" crop-recommendation-app

echo "Application is now running at http://localhost:8080"
