resource "aws_iam_role" "packer" {
  name = "stress-app-packer"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "ec2.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })

  tags = {
    Name = "stress-app-packer"
  }
}

resource "aws_iam_role_policy" "packer_policy" {
  name = "stress-app-packer-policy"
  role = aws_iam_role.packer.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      # Required for Packer to build AMIs
      {
        Effect = "Allow",
        Action = [
          "ec2:*",
          "iam:PassRole",
          "ssm:GetParameters",
          "ssm:GetParameter",
          "ssm:DescribeParameters",
          "kms:Decrypt",
          "kms:Encrypt",
          "kms:GenerateDataKey",
          "kms:DescribeKey",
          "logs:*",
          "cloudwatch:*"
        ],
        Resource = "*"
      }
    ]
  })
}
