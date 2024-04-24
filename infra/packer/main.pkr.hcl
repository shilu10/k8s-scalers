packer {
  required_plugins {
    amazon = {
      version = ">= 1.0.0"
      source  = "github.com/hashicorp/amazon"
    }
    ansible = {
      version = ">= 1.0.0"
      source  = "github.com/hashicorp/ansible"
    }
  }
}

source "amazon-ebs" "ubuntu" {
  ami_name      = "ubuntu-22-04-custom-{{timestamp}}"
  instance_type = "t2.micro"
  region        = var.aws_region
  source_ami    = var.source_ami
  ssh_username  = "ubuntu"
  communicator  = "ssh"

  ssh_keypair_name     = var.ssh_key_name
  ssh_private_key_file = "scripts/${var.ssh_key_name}.pem"

  assume_role {
    role_arn     = var.packer_role_arn
    session_name = "packer-session"
  }

  tags = {
    Name = "stress-app-Ubuntu-AMI"
  }
}

build {
  sources = ["source.amazon-ebs.ubuntu"]

  provisioner "shell" {
    script = "scripts/shell.sh"
  }

  # Uncomment if using Ansible
  # provisioner "ansible" {
  #   playbook_file = "ansible/playbook.yaml"
  # }
}
