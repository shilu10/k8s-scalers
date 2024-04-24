
resource "aws_ecr_repository" "repos" {
  for_each = {
    for idx, repo in var.ecr_repos :
    repo.name => repo
  }
  name                 = each.value.name
  image_tag_mutability = each.value.image_tag_mutability

  image_scanning_configuration {
    scan_on_push = each.value.scan_on_push
  }

  tags = var.stress_app_tags
}


resource "local_file" "image_push_script" {
  filename = "${path.module}/scripts/image_push.sh"

  content = <<-EOT
%{for repo_name, repo in aws_ecr_repository.repos~}
docker tag ${replace(repo_name, "-", "_")}:latest ${repo.repository_url}:latest
docker push ${repo.repository_url}:latest
%{endfor~}

EOT

  file_permission = "0755"
}


resource "null_resource" "push_images" {
  provisioner "local-exec" {
      command = file("scripts/image_push.sh")
  }
}

#variable "repo_names" {
#  type    = list(string)
#  default = ["upload_service", "auth_service", "caption_service", "caption_worker", "gateway_service", "object_creator", "email_notifier"]  # <-- Replace with your actual ECR repo names
#}

# Loop over each repository name to get its details
#data "aws_ecr_repository" "repos" {
#  for_each = toset(var.repo_names)
#  name     = each.key
#}
