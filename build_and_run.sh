#!/bin/bash

# Exit on any error
set -e

# Build the Docker image
echo "Building the Docker image..."
docker build -t crop-recommendation-app .

# Run the Docker container
echo "Running the Docker container on port 5000..."
echo "To stop it later, use 'docker ps' to find the container ID and 'docker stop <id>'"
docker run -d -p 5000:5000 -e GEMINI_API_KEY="AIzaSyA41_i64ESFdHL2oQy2VlmqnjEnWB88K3M" crop-recommendation-app

echo "Application is now running at http://localhost:5000"
