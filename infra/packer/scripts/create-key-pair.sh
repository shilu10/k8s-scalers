#!/bin/bash

KEY_NAME="stress-app"
KEY_FILE="${KEY_NAME}.pem"
REGION="us-east-1"

# 1. Generate a new key pair locally (private + public key)
echo "🔐 Generating SSH key pair..."
ssh-keygen -t rsa -b 4096 -f "$KEY_FILE" -N ""

# 2. Import the public key to AWS EC2 as a key pair
echo "☁️  Uploading public key to AWS..."
aws ec2 import-key-pair \
  --key-name "$KEY_NAME" \
  --public-key-material fileb://"${KEY_FILE}.pub" \
  --region "$REGION"

# 3. Set proper permissions for the private key
chmod 400 "$KEY_FILE"

echo "✅ SSH key pair '$KEY_NAME' created and uploaded to AWS EC2."
echo "🔑 Private key: $KEY_FILE"
echo "📁 Public key:  ${KEY_FILE}.pub"
