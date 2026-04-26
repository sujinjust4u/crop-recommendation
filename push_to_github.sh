#!/bin/bash

# Check if a GitHub username/repo was provided
if [ -z "$1" ]; then
  echo "Usage: ./push_to_github.sh <your_github_username>/<your_repo_name>"
  echo "Example: ./push_to_github.sh sujinsp/seai-crop-recommendation"
  exit 1
fi

GITHUB_REPO=$1

# Exit on any error
set -e

# Rename branch to main if it's not already
git branch -M main

# Remove the old remote origin (since we cloned from someone else)
git remote remove origin || true

# Add your new remote repository
git remote add origin "https://github.com/${GITHUB_REPO}.git"

# Push to your GitHub repository
echo "Pushing code to https://github.com/${GITHUB_REPO}..."
git push -u origin main

echo "Successfully pushed the application to GitHub!"
