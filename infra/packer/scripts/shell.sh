#!/bin/bash

# Update and install prerequisites
sudo apt update -y && sudo apt upgrade -y 
sudo apt-get install -y lsb-release curl gpg

# Add Redis repository
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
sudo chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

# Install Redis
sudo apt-get update
sudo apt-get install -y redis

# Modify Redis config to allow remote access
sudo sed -i "s/^bind .*/bind 0.0.0.0/" /etc/redis/redis.conf
sudo sed -i "s/^protected-mode .*/protected-mode no/" /etc/redis/redis.conf

# Enable and restart Redis
sudo systemctl enable redis-server
sudo systemctl restart redis-server
