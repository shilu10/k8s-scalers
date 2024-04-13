
resource "aws_ecr_repository" "repos" {
  for_each = {
    for idx, repo in var.ecr_repos :
        repo.name => repo
  }
    name = each.value.name
    image_tag_mutability = each.value.image_tag_mutability

    image_scanning_configuration {
      scan_on_push = each.value.scan_on_push
    }
}


resource "local_file" "image_push_script" {
  filename = "${path.module}/scripts/image_push.sh"

  content = <<-EOT
%{ for repo_name, repo in aws_ecr_repository.repos ~}
docker tag ${replace(repo_name, "-", "_")}:latest ${repo.repository_url}:latest
docker push ${repo.repository_url}:latest
%{ endfor ~}

EOT

  file_permission = "0755"
}


resource "null_resource" "push_images" {
 
  provisioner "local-exec" {
    command = file("scripts/image_push.sh")
  }

}

#### lambda functions

locals {
  target_repos      = ["object_creator", "email_notifier"]
}

resource "aws_iam_role" "lambda_roles" {
  for_each = toset(local.target_repos)

  name = "${each.key}_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

locals {
  object_creator_action = ["s3:PutObject", 
                          "logs:CreateLogGroup",
                          "logs:CreateLogStream",
                          "logs:PutLogEvents"
                        ]

  email_notifier_action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
}

resource "aws_iam_role_policy" "object_creator" {
  name   = var.caption_worker_iam_policy_name
  role   = aws_iam_role.lambda_roles["object_creator"].id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Action = local.object_creator_action
      Resource = [
        var.stress_app_bucket_arn,
        "arn:aws:logs:*:*:*"
      ]
    }]
  })
}

resource "aws_iam_role_policy" "email_notifier" {
  name = "lambda_basic_logging"
  role = aws_iam_role.lambda_roles["email_notifier"].id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = local.email_notifier_action,
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

locals {
  lambda_function_env_vars = {
    object_creator = {
      BUCKET_NAME = var.stress_app_bucket_arn
    }

    email_notifier = {
      FROM_EMAIL = var.from_email
      APP_PASSWORD = var.google_app_password
    }
  }
}

resource "aws_lambda_function" "stress_app" {
  for_each = {
    for repo_name, repo in aws_ecr_repository.repos :
    repo_name => repo if contains(local.target_repos, repo_name)
  }

  function_name = "lambda_${each.key}"
  description   = "Lambda function for ${each.key}"
  image_uri     = "${each.value.repository_url}:latest"
  timeout       = 30
  memory_size   = 128
  publish       = true
  package_type  = "Image"

  environment {
    variables = local.lambda_function_env_vars[each.key]
  }
  role = aws_iam_role.lambda_roles[each.key].arn
}


resource "aws_sns_topic" "stress_app" {
  name = var.stress_app_topic_name
}


resource "aws_sns_topic_subscription" "stress_app_lambda" {
  for_each = {
    for lambda_name, lambda in aws_lambda_function.stress_app :
    lambda_name => lambda
  }

  topic_arn = aws_sns_topic.stress_app.arn
  protocol  = "lambda"
  endpoint  = each.value.arn
}




