terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }

    mongodbatlas = {
      source  = "mongodb/mongodbatlas"
      version = "~> 1.16.0"
    }

    cloudamqp = {
      source = "cloudamqp/cloudamqp"
      version = "1.34.0"
    }
    
  }
}
