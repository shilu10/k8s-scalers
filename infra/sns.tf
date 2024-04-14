## setup of sns for auth-service (when user creates a account, auth-service sends event to this topic and it has two lambda subscription)

resource "aws_sns_topic" "stress_app" {
  name = var.stress_app_topic_name

  tags = var.stress_app_tags
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