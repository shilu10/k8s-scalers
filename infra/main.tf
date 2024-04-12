
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = var.vpc_name
  cidr = var.vpc_cidr

  azs             = var.azs
  public_subnets  = var.public_subnets

  tags = var.vpc_tags
}


resource "aws_eks_cluster" "this" {
  name     = var.eks_cluster_name
  role_arn = aws_iam_role.eks.arn

  version  = var.eks_version

  vpc_config {
    subnet_ids = module.vpc.public_subnets
  }

  # Ensure that IAM Role permissions are created before and deleted after EKS Cluster handling.
  # Otherwise, EKS will not be able to properly delete EKS managed EC2 infrastructure such as Security Groups.
  depends_on = [
    aws_iam_role_policy_attachment.cluster_AmazonEKSClusterPolicy,
  ]
}


resource "aws_iam_role" "eks" {
  name = var.eks_iam_role_name
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "sts:AssumeRole",
          "sts:TagSession"
        ]
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      },
    ]
  })
}


resource "aws_iam_role_policy_attachment" "cluster_AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks.name
}


#### node group

resource "aws_eks_node_group" "this" {
  cluster_name    = aws_eks_cluster.this.name
  node_group_name = var.node_group_name
  node_role_arn   = aws_iam_role.node_group.arn
  subnet_ids      = module.vpc.public_subnets

  instance_types = var.ng_instance_type

  scaling_config {
    desired_size = var.ng_desired_size
    max_size     = var.ng_max_size
    min_size     = var.ng_min_size
  }

  update_config {
    max_unavailable = var.ng_max_unavailable
  }

  # Ensure that IAM Role permissions are created before and deleted after EKS Node Group handling.
  # Otherwise, EKS will not be able to properly delete EC2 Instances and Elastic Network Interfaces.
  depends_on = [
    aws_iam_role_policy_attachment.ng-AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.ng-AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.ng-AmazonEC2ContainerRegistryReadOnly,
  ]
}


resource "aws_iam_role" "node_group" {
  name = var.ng_iam_role_name

  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
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


### iam role for service account

data "aws_eks_cluster" "this" {
  name = aws_eks_cluster.this.name
}

data "aws_eks_cluster_auth" "this" {
  name = aws_eks_cluster.this.name
}

data "aws_iam_openid_connect_provider" "this" {
  url = replace(data.aws_eks_cluster.this.identity[0].oidc[0].issuer, "https://", "")
  
  depends_on = [aws_eks_cluster.this]
}



resource "aws_iam_policy" "app_policy" {
  name        = var.service_account_iam_policy_name
  description = var.service_account_iam_policy_description
  policy      = data.aws_iam_policy_document.app_policy.json
}


data "aws_iam_policy_document" "app_policy" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["arn:aws:s3:::*/*"]
  }
}


module "irsa_role" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "~> 5.0"

  role_name = var.irsa_role_name

  role_policy_arns = {
    app_policy = aws_iam_policy.app_policy.arn
  }

  oidc_providers = {
    main = {
      provider_arn               = data.aws_iam_openid_connect_provider.this.arn
      namespace_service_accounts = ["default:app-service-account"]
    }
  }
}


resource "kubernetes_service_account" "app" {
  metadata {
    name      = var.service_account_name
    namespace = var.sa_namespace
    annotations = {
      "eks.amazonaws.com/role-arn" = module.irsa_role.iam_role_arn
    }
  }
}

