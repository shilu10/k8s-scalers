packer {
  required_plugins {
    amazon = {
      source  = "github.com/hashicorp/amazon"
      version = "~> 1"
    }
  }
}


variable "aws_region" {
  type    = string
  default = "us-east-1"
}

source "amazon-ebs" "ubuntu" {
  ami_name      = "ubuntu-22-04-custom-{{timestamp}}"
  instance_type = "t2.micro"
  region        = var.aws_region
  source_ami    = "ami-0f9de6e2d2f067fca"
  ssh_username  = "ubuntu"
  communicator  = "ssh"

  assume_role {
      role_arn     = "arn:aws:iam::533267453751:role/for-stress-app-packer"
      session_name = "SESSION_NAME"
  }
  
  # Specify the SSH key pair for the EC2 instance
  ssh_keypair_name      = "stress-app"          # Name of your key pair
  ssh_private_key_file  = "stress-app.pem"  # Path to your private key

  tags = {
    Name = "stress-app-Ubuntu-AMI"
  }
}

build {
  sources = ["source.amazon-ebs.ubuntu"]

  provisioner "shell" {
    script = "shell.sh"
  }
}
