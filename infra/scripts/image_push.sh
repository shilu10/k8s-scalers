#!/bin/bash
set -e


AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)

docker tag auth_service:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/auth_service:latest
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/auth_service:latest
docker tag caption_service:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/caption_service:latest
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/caption_service:latest
docker tag caption_worker:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/caption_worker:latest
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/caption_worker:latest
docker tag email_notifier:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/email_notifier:latest
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/email_notifier:latest
docker tag gateway_service:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/gateway_service:latest
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/gateway_service:latest
docker tag object_creator:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/object_creator:latest
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/object_creator:latest
docker tag upload_service:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/upload_service:latest
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/upload_service:latest

