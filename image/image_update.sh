#!/bin/bash

#configuration
IMAGE_NAME="aws_scrapy_real_estate"
AWS_REGION="eu-north-1"
AWS_ACCOUNT="442042537983"
ECR_REPO="${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"
ECR_IMAGE="${ECR_REPO}/${IMAGE_NAME}"


#build docker image
docker build --no-cache --platform linux/amd64 -t ${IMAGE_NAME} .

#authenticate aws
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}

#tag docker image
docker tag ${IMAGE_NAME}:latest ${ECR_IMAGE}:latest

#push image to AWS repository
docker push ${ECR_IMAGE}:latest