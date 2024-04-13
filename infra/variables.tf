variable "vpc_cidr" {
    type = string 
    default = "10.0.0.0/16"
}


variable "azs" {
    type = list(string)
    default = [ "us-east-1a", "us-east-1b", "us-east-1c" ]
}


variable "public_subnets" {
    type = list(string)
    default = [ "10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24" ]

    validation {
      condition     = length(var.azs) == length(var.public_subnets)
      error_message = "public_subnets must be the same length as azs"
    }
}


variable "vpc_name" {
  type = string
  default = "stress-app"
}

variable "vpc_tags" {
  type = map(string)
  default =  {
    Terraform = "true"
    Environment = "dev"
    App = "Stress"
  }
}


variable "eks_cluster_name" {
    type = string 
    default = "stress-app-cluster"
}


variable "eks_iam_role_name" {
    type = string 
    default = "stress-app-eks-role"
}


# node group

variable "node_group_name" {
  type = string
  default = "stress-app-ng-1"
}


variable "ng_desired_size" {
  type = number
  default = 1
}


variable "ng_max_size" {
  type = number
  default = 2 
}

variable "ng_min_size" {
  type = number
  default = 1
}

variable "ng_max_unavailable" {
  type = number
  default = 1 
}

variable "ng_iam_role_name" {
  type = string
  default = "stress-app-ng-role"
}

variable "ng_instance_type" {
  type = list(string)
  default = ["t2.micro"]
}

variable "eks_version" {
  type = string
  default = "1.31"
}

variable "service_account_iam_policy_name" {
  type = string
  default = "demo"
}

variable "service_account_iam_policy_description" {
  type = string
  default = "testing purpose"
}

variable "irsa_role_name" {
  type = string
  default = "demo-irsa-role"
}

variable "service_account_name" {
  type = string
  default = "demo"
}

variable "sa_namespace" {
  type = string
  default = "dev"
}

variable "private_subnets" {
  type = list(string)
    default = [ "10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24" ]

    validation {
      condition     = length(var.azs) == length(var.private_subnets)
      error_message = "public_subnets must be the same length as azs"
    }

}


variable "mysqldb_username" {
  default = "admin"
}

variable "mysqldb_password" {
  default = "your_secure_password"  # Avoid hardcoding in production; use secrets manager or env vars
}

variable "mysqldb_name" {
  default = "stress"
}

variable "mysqldb_instance_class" {
  default = "db.t3.micro"
}

variable "mysql_allocated_storage" {
  default = 20
}


variable "mysql_db_subnet_group_name" {
  type = string
  default = "stress-app-mysql-sg"
}

variable "mysql_tags" {
  type = map(string)
  default = {
    "env": "dev",
    "app": "mysql"
  }
}

variable "mysql_sg_name" {
  type = string
  default = "stress-sg"
}

variable "mysql_sg_description" {
  type = string
  default = "Allowing all inbound and outbound connection only for testing"
}

variable "aws_ec2_tag_values" {
  type = list(string)
  default = ["stress-app-Ubuntu-AMI"]
}

variable "redis_ec2_instance_type" {
  type = string
  default = "t2.micro"
}

variable "redis_ec2_tags" {
  type = map(string)
  default = {
    "Env": "Dev",
    "App": "Redis-Instance"
  }
}

variable "caption_worker_iam_role_name" {
  type = string
  default = "stress_app_caption_worker_iam_role_irsa"
}

variable "caption_worker_iam_policy_name" {
  type = string
  default = "stress_app_caption_worker_iam_policy_irsa"
}

variable "stress_app_bucket_arn" {
  type = string 
  default = "arn:aws:s3:::stress-app-video-bucket-example"
}

variable "caption_worker_sa_name" {
 type = string 
 default = "caption-worker-sa"
}

variable "upload_service_iam_role_name" {
  type = string
  default = "stress_app_upload_service_iam_role_irsa"
}

variable "upload_service_iam_policy_name" {
  type = string 
  default = "stress_app_upload_service_iam_policy_irsa"
}

variable "upload_service_iam_action" {
  type = list(string)
  default = ["s3:PutObject",
                "s3:GetObject",
                "s3:ListBucketMultipartUploads",
                "s3:AbortMultipartUpload",
                "s3:ListMultipartUploadParts"]
}

variable "upload_service_sa_name" {
  type = string
  default = "upload-service-sa"
}

variable "upload_service_db" {
  type = string 
  default = "upload-service-db"
}

# ecr registry
variable "ecr_repos" {
  type = list(map(string))

  default = [
    {
      name = "upload_service",
      image_tag_mutability = "MUTABLE",
      scan_on_push = true
    },

    {
      name = "email_notifier",
      image_tag_mutability = "MUTABLE",
      scan_on_push = true
    },

    {
      name = "auth_service",
      image_tag_mutability = "MUTABLE",
      scan_on_push = true
    },

    {
      name = "gateway_service",
      image_tag_mutability = "MUTABLE",
      scan_on_push = true
    },

    {
      name = "caption_service",
      image_tag_mutability = "MUTABLE",
      scan_on_push = true
    },

    {
      name = "caption_worker",
      image_tag_mutability = "MUTABLE",
      scan_on_push = true
    },

    {
      name = "object_creator",
      image_tag_mutability = "MUTABLE",
      scan_on_push = true
    }
  ]
}

variable "stress_app_topic_name" {
  type = string
  default = "stress_app_auth_service_topic"
}

variable "google_app_password" {
  type = string
  default ="dummy"
}

variable "stress_app_bucket_name" {
  type = string
  default = "stress-app-video-bucket-example"
}

variable "from_email" {
  type = string
  default = "dummy@gmail.com"
}