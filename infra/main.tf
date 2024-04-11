provider "aws" {
  region = "us-east-1"

}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.this.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.this.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.this.token
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = var.vpc_name
  cidr = var.vpc_cidr

  azs             = var.azs
  public_subnets  = var.public_subnets
  private_subnets = var.private_subnets

  map_public_ip_on_launch = true

  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = var.vpc_tags
}

resource "aws_iam_role" "eks" {
  name = var.eks_iam_role_name
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = ["sts:AssumeRole", "sts:TagSession"],
      Effect = "Allow",
      Principal = { Service = "eks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "cluster_AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks.name
}

resource "aws_eks_cluster" "this" {
  name     = var.eks_cluster_name
  role_arn = aws_iam_role.eks.arn
  version  = var.eks_version

  vpc_config {
    subnet_ids = module.vpc.public_subnets
  }

  depends_on = [aws_iam_role_policy_attachment.cluster_AmazonEKSClusterPolicy]
}

data "aws_eks_cluster" "this" {
  name       = aws_eks_cluster.this.name
  depends_on = [aws_eks_cluster.this]
}

data "aws_eks_cluster_auth" "this" {
  name       = aws_eks_cluster.this.name
  depends_on = [aws_eks_cluster.this]
}

resource "aws_iam_role" "node_group" {
  name = var.ng_iam_role_name
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ng-AmazonEKSWorkerNodePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.node_group.name
}

resource "aws_iam_role_policy_attachment" "ng-AmazonEKS_CNI_Policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.node_group.name
}

resource "aws_iam_role_policy_attachment" "ng-AmazonEC2ContainerRegistryReadOnly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.node_group.name
}

resource "aws_eks_node_group" "this" {
  cluster_name    = aws_eks_cluster.this.name
  node_group_name = var.node_group_name
  node_role_arn   = aws_iam_role.node_group.arn
  subnet_ids      = module.vpc.public_subnets
  instance_types  = var.ng_instance_type

  scaling_config {
    desired_size = var.ng_desired_size
    max_size     = var.ng_max_size
    min_size     = var.ng_min_size
  }

  update_config {
    max_unavailable = var.ng_max_unavailable
  }

  depends_on = [
    aws_iam_role_policy_attachment.ng-AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.ng-AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.ng-AmazonEC2ContainerRegistryReadOnly
  ]
}

### IRSA Setup

data "tls_certificate" "this" {
  url = data.aws_eks_cluster.this.identity[0].oidc[0].issuer
}

resource "aws_iam_openid_connect_provider" "this" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.this.certificates[0].sha1_fingerprint]
  url             = data.aws_eks_cluster.this.identity[0].oidc[0].issuer
}

resource "aws_iam_role" "this" {
  name = "eks-irsa-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Federated = aws_iam_openid_connect_provider.this.arn
      },
      Action = "sts:AssumeRoleWithWebIdentity",
      Condition = {
        StringEquals = {
          "${aws_iam_openid_connect_provider.this.url}:sub" = "system:serviceaccount:${var.sa_namespace}:${var.service_account_name}",
          "${aws_iam_openid_connect_provider.this.url}:aud" = "sts.amazonaws.com"
        }
      }
    }]
  })
}

resource "aws_iam_role_policy" "this" {
  name   = "eks-irsa-policy"
  role   = aws_iam_role.this.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Action = ["s3:ListBucket", "s3:GetObject"],
      Resource = "*"
    }]
  })
}

resource "kubernetes_namespace" "irsa_ns" {
  metadata {
    name = var.sa_namespace
  }
}

resource "kubernetes_service_account" "app" {
  metadata {
    name      = var.service_account_name
    namespace = var.sa_namespace
    annotations = {
      "eks.amazonaws.com/role-arn" = aws_iam_role.this.arn
    }
  }

  depends_on = [kubernetes_namespace.irsa_ns]
}

### RDS Setup

resource "aws_db_subnet_group" "default" {
  name       = var.mysql_db_subnet_group_name
  subnet_ids = module.vpc.private_subnets
  tags       = var.mysql_tags
}

resource "aws_security_group" "rds_sg" {
  name        = var.mysql_sg_name
  description = var.mysql_sg_description
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Only for testing
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "mysql" {
  identifier              = "my-mysql-db"
  engine                  = "mysql"
  engine_version          = "8.0"
  instance_class          = var.mysqldb_instance_class
  allocated_storage       = var.mysql_allocated_storage
  db_name                 = var.mysqldb_name
  username                = var.mysqldb_username
  password                = var.mysqldb_password
  db_subnet_group_name    = aws_db_subnet_group.default.name
  vpc_security_group_ids  = [aws_security_group.rds_sg.id]
  skip_final_snapshot     = true
  publicly_accessible     = true
  storage_encrypted       = true
  multi_az                = false

  tags = {
    Name = "MySQL-RDS"
  }
}
