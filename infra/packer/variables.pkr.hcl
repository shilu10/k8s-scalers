variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "ssh_key_name" {
  type    = string
  default = "stress-app"
}

variable "packer_role_arn" {
  type    = string
}

variable "source_ami" {
  type    = string
  default = "ami-0f9de6e2d2f067fca"  # Ubuntu 22.04 (update as needed)
}
