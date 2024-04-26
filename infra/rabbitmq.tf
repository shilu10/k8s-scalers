## RabbitMQ Cloud

# Configure the CloudAMQP Provider
provider "cloudamqp" {
  apikey                         = "xxx"
  enable_faster_instance_destroy = true  
}

# Create a new CloudAMQP instance (Free Tier)
resource "cloudamqp_instance" "instance" {
  name   = var.cloudamqp_instance_name
  plan   = "lemur"  # Correct free-tier plan
  region = "amazon-web-services::us-west-1"  # Ensure region supports free-tier
  tags   = var.cloudamqp_instance_tags
}


# New recipient to receive notifications
resource "cloudamqp_notification" "recipient_01" {
  instance_id = cloudamqp_instance.instance.id
  type        = "email"
  value       = var.cloudamqp_notification_email
  name        = "alarm"
}



