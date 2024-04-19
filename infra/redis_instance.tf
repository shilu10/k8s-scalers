data "aws_ami" "latest" {
  filter {
    name   = "tag:Name"
    values = ["stress-app-Ubuntu-AMI"]
  }

  most_recent = true
  owners      = ["self"]
}

resource "aws_instance" "redis" {
  ami                    = data.aws_ami.latest.id
  instance_type          = var.redis_ec2_instance_type
  subnet_id              = module.vpc.private_subnets[0]
  vpc_security_group_ids = [aws_security_group.redis_sg.id]

  tags = var.stress_app_tags
}


resource "aws_security_group" "redis_sg" {
  name        = "redis-sg"
  description = "Allow Redis access from EKS worker nodes"
  vpc_id      = module.vpc.vpc_id

  tags = var.stress_app_tags
}

# Allow Redis access from EKS node SG
resource "aws_security_group_rule" "redis_from_eks" {
  type                     = "ingress"
  from_port                = 6379
  to_port                  = 6379
  protocol                 = "tcp"
  security_group_id        = aws_security_group.redis_sg.id
  # source_security_group_id = aws_security_group.eks_nodes_sg.id  this is more granular than vpc cidr
  cidr_blocks       = [module.vpc.vpc_cidr_block]
}


