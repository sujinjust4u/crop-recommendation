#!/bin/bash

# Check if a DockerHub username was provided
if [ -z "$1" ]; then
  echo "Usage: ./push_to_dockerhub.sh <your_dockerhub_username>"
  exit 1
fi

DOCKERHUB_USERNAME=$1
IMAGE_NAME="crop-recommendation-app"
TAG="latest"

# Exit on any error
set -e

# Prompt for Docker login if not already logged in
echo "Logging into DockerHub..."
docker login -u "$DOCKERHUB_USERNAME"

# Tag the local image for DockerHub
echo "Tagging the image..."
docker tag $IMAGE_NAME:$TAG $DOCKERHUB_USERNAME/$IMAGE_NAME:$TAG

# Push the image to DockerHub
echo "Pushing the image to DockerHub repository: $DOCKERHUB_USERNAME/$IMAGE_NAME:$TAG..."
docker push $DOCKERHUB_USERNAME/$IMAGE_NAME:$TAG

echo "Successfully pushed the application to DockerHub!"
echo "It can now be pulled using: docker pull $DOCKERHUB_USERNAME/$IMAGE_NAME:$TAG"
