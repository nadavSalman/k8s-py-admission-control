#!/bin/bash
set -x

# docker rm py-admission-webhook && docker build -t py-admission-webhook:latest . && docker run -it --name py-admission-webhook py-admission-webhook:latest q


# Define variables
ECR_PREFIX="XXXXXXXXXXXXX.dkr.ecr.eu-west-1.amazonaws.com"
APP_REPOSITORY="py-admission-webhook"
ECR_REPOSITORY="$ECR_PREFIX/$APP_REPOSITORY"
TAG="latest"


# Authenticate Docker to the Amazon ECR registry
aws ecr get-login-password --region eu-west-1 --profile dev | docker login --username AWS --password-stdin $ECR_PREFIX


# Remove existing container
docker rm py-admission-webhook

# Build the Docker image
docker build -t $ECR_REPOSITORY:$TAG .

# Tag the Docker image for ECR
docker tag  $ECR_REPOSITORY:$TAG


# Generate a random tag
RANDOM_TAG=$(date +%s)

# Tag the Docker image with the random tag
# docker tag  $ECR_REPOSITORY:$RANDOM_TAG
# docker tag  $ECR_REPOSITORY:$RANDOM_TAG

# Delete the image tagged 'latest' from the ECR repository
aws ecr batch-delete-image --repository-name $APP_REPOSITORY --image-ids imageTag=latest --region eu-west-1 --profile dev


# Push the Docker image to ECR
docker push $ECR_REPOSITORY:$TAG

