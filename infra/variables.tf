variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "azs" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "public_subnets" {
  type    = list(string)
  default = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]

  validation {
    condition     = length(var.azs) == length(var.public_subnets)
    error_message = "public_subnets must be the same length as azs"
  }
}

variable "vpc_name" {
  type    = string
  default = "stress-app"
}

variable "eks_cluster_name" {
  type    = string
  default = "stress-app-cluster"
}

variable "eks_iam_role_name" {
  type    = string
  default = "stress_app_eks_role"
}

# node group

variable "node_group_name" {
  type    = string
  default = "stress-app-ng-1"
}

variable "ng_desired_size" {
  type    = number
  default = 1
}

variable "ng_max_size" {
  type    = number
  default = 2
}

variable "ng_min_size" {
  type    = number
  default = 1
}

variable "ng_max_unavailable" {
  type    = number
  default = 1
}

variable "ng_iam_role_name" {
  type    = string
  default = "stress_app_ng_role"
}

variable "ng_instance_type" {
  type    = list(string)
  default = ["t3.medium"]
}

variable "eks_version" {
  type    = string
  default = "1.31"
}

variable "sa_namespace" {
  type    = string
  default = "dev"
}

variable "private_subnets" {
  type    = list(string)
  default = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]

  validation {
    condition     = length(var.azs) == length(var.private_subnets)
    error_message = "private_subnet must be the same length as azs"
  }

}

variable "mysqldb_username" {
  type = string 
  default = "admin"
}

variable "mysqldb_password" {
  type = string 
  default = "your_secure_password" # Avoid hardcoding in production; use secrets manager or env vars
}

variable "mysqldb_name" {
  type = string 
  default = "stress"
}

variable "mysqldb_instance_class" {
  type = string 
  default = "db.t3.micro"
}

variable "mysql_allocated_storage" {
  default = 20
}


variable "mysql_db_subnet_group_name" {
  type    = string
  default = "stress-app-mysql-sg"
}

variable "mysql_sg_name" {
  type    = string
  default = "stress-sg"
}

variable "mysql_sg_description" {
  type    = string
  default = "Allowing all inbound and outbound connection only for testing"
}

variable "aws_ec2_tag_values" {
  type    = list(string)
  default = ["stress-app-Ubuntu-AMI"]
}

variable "redis_ec2_instance_type" {
  type    = string
  default = "t2.micro"
}

variable "redis_ec2_tags" {
  type = map(string)
  default = {
    "Env" : "Dev",
    "App" : "Redis-Instance"
  }
}

variable "caption_worker_iam_role_name" {
  type    = string
  default = "caption_worker_role"
}

variable "caption_worker_iam_policy_name" {
  type    = string
  default = "caption_worker_policy"
}


variable "caption_worker_sa_name" {
  type    = string
  default = "caption-sa"
}

variable "upload_service_iam_role_name" {
  type    = string
  default = "upload_service_role"
}

variable "upload_service_iam_policy_name" {
  type    = string
  default = "upload_service_policy"
}

variable "upload_service_sa_name" {
  type    = string
  default = "upload-sa"
}

variable "upload_service_db" {
  type    = string
  default = "upload-service-db"
}

# ecr registry
variable "ecr_repos" {
  type = list(map(string))

  default = [
    {
      name                 = "upload_service",
      image_tag_mutability = "MUTABLE",
      scan_on_push         = true
    },

    {
      name                 = "email_notifier",
      image_tag_mutability = "MUTABLE",
      scan_on_push         = true
    },

    {
      name                 = "auth_service",
      image_tag_mutability = "MUTABLE",
      scan_on_push         = true
    },

    {
      name                 = "gateway_service",
      image_tag_mutability = "MUTABLE",
      scan_on_push         = true
    },

    {
      name                 = "caption_service",
      image_tag_mutability = "MUTABLE",
      scan_on_push         = true
    },

    {
      name                 = "caption_worker",
      image_tag_mutability = "MUTABLE",
      scan_on_push         = true
    },

    {
      name                 = "object_creator",
      image_tag_mutability = "MUTABLE",
      scan_on_push         = true
    }
  ]
}

variable "stress_app_topic_name" {
  type    = string
  default = "stress_app_auth_service_topic"
}

variable "google_app_password" {
  type    = string
  default = "xxxx"
  sensitive = true

}

variable "stress_app_bucket_name" {
  type    = string
  default = "stress-app-video-bucket-example-1"
}

variable "from_email" {
  type    = string
  default = "dummy@gmail.com"
}

variable "stress_app_tags" {
  type = map(string)
  default = {
    Env = "dev",
    App = "stress-app"
    "karpenter.sh/discovery" = var.eks_cluster_name
  }
}

variable "mongodb_atlas_org_id" {
  description = "MongoDB Atlas Organization ID"
  type        = string
  default = "xxx"
}

variable "project_name" {
  description = "Name of the MongoDB Atlas Project"
  type        = string
  default     = "stress_app"
}

variable "cloudamqp_instance_name" {
  type = string
  default = "stress_app"
}

variable "cloudamqp_instance_tags" {
  type = list(string)
  default = [ "stress-app" ]
}

variable "cloudamqp_notification_email" {
  type = string
  default = "dummy@gmail.com"
}

variable "rds_sg_name" {
  type = string
  default = "stress-app-rds"
}

variable "auth_service_iam_role_name" {
  type = string 
  default = "auth_service_role"
}

variable "auth_service_sa_name" {
  type = string 
  default = "auth-sa"
}

variable "auth_service_policy_name" {
  type =string
  default = "auth_service_policy"
}

### aws mq 
variable "rabbitmq_broker_name" {
  type = string 
  default = "stress-app-mq"
}

variable "rabbitmq_engine_version" {
  type = string 
  default = "3.13"
}

variable "rabbitmq_host_instance_type" {
  type = string 
  default = "mq.t3.micro"
}

variable "rabbitmq_deployment_mode" {
  type = string 
  default = "SINGLE_INSTANCE"
}

variable "rabbit_mq_username" {
  type = string 
  default = "shilash"
}

variable "rabbit_mq_password" {
  type = string 
  default = "xxx"
}

# karpenter 
variable "default_instance_profile" {
  type    = string
  default = "KarpenterNodeInstanceProfile-stress-app-cluster"
}

# amplify
variable "github_token" {
  type      = string
  sensitive = true
}

# packer 
output "packer_role_arn" {
  value = aws_iam_role.packer.arn
}
