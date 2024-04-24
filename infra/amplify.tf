
resource "aws_amplify_app" "k8s_scalers" {
  name = "k8s-scalers-app"
  repository = "https://github.com/shilu10/k8s-scalers.git"
  oauth_token = var.github_token

  build_spec = <<EOF
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - cd src/frontend
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: src/frontend/build
    files:
      - '**/*'
  cache:
    paths:
      - src/frontend/node_modules/**/*
EOF

  platform = "WEB"
}

resource "aws_amplify_branch" "main" {
  app_id = aws_amplify_app.k8s_scalers.id
  branch_name = "main"
  stage = "PRODUCTION"
}
