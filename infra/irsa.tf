provider "kubernetes" {
  host                   = data.aws_eks_cluster.this.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.this.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.this.token
}


### IRSA Setup

### service account for caption-worker
resource "kubernetes_namespace" "irsa" {
  metadata {
    name = var.sa_namespace
  }
}

data "tls_certificate" "this" {
  url = data.aws_eks_cluster.this.identity[0].oidc[0].issuer
}

resource "aws_iam_openid_connect_provider" "this" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.this.certificates[0].sha1_fingerprint]
  url             = data.aws_eks_cluster.this.identity[0].oidc[0].issuer

  tags = var.stress_app_tags
}


resource "aws_iam_role" "caption_worker" {
  name = var.caption_worker_iam_role_name
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
          "${aws_iam_openid_connect_provider.this.url}:sub" = "system:serviceaccount:${var.sa_namespace}:${var.caption_worker_sa_name}",
          "${aws_iam_openid_connect_provider.this.url}:aud" = "sts.amazonaws.com"
        }
      }
    }]
  })

  tags = var.stress_app_tags
}


locals {
  caption_worker_iam_actions = [
    "s3:GetObject",
    "s3:ListObject"
  ]
}

resource "aws_iam_role_policy" "caption_worker" {
  name = var.caption_worker_iam_policy_name
  role = aws_iam_role.caption_worker.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action   = local.caption_worker_iam_actions
      Resource = "${module.s3_bucket.s3_bucket_arn}/*" # need /* "${module.s3_bucket.s3_bucket_arn}/*"
    }]
  })
}

resource "kubernetes_service_account" "caption_worker" {
  metadata {
    name      = var.caption_worker_sa_name
    namespace = var.sa_namespace
    annotations = {
      "eks.amazonaws.com/role-arn" = aws_iam_role.caption_worker.arn
    }
  }

  depends_on = [kubernetes_namespace.irsa]
}


### service account for upload-service

resource "aws_iam_role" "upload_service" {
  name = var.upload_service_iam_role_name
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
          "${aws_iam_openid_connect_provider.this.url}:sub" = "system:serviceaccount:${var.sa_namespace}:${var.upload_service_sa_name}",
          "${aws_iam_openid_connect_provider.this.url}:aud" = "sts.amazonaws.com"
        }
      }
    }]
  })

  tags = var.stress_app_tags
}


locals{
  upload_service_actions = [
        "s3:PutObject",
        "s3:PutObjectAcl",
        "s3:GetObject",
        "s3:ListMultipartUploadParts",
        "s3:AbortMultipartUpload",
      
  ]
} 


resource "aws_iam_role_policy" "upload_service" {
  name = var.upload_service_iam_policy_name
  role = aws_iam_role.upload_service.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action   = local.upload_service_actions
      Resource = "${module.s3_bucket.s3_bucket_arn}/*"   # /* at end of this
    }]
  })
}

resource "kubernetes_service_account" "upload_service" {
  metadata {
    name      = var.upload_service_sa_name
    namespace = var.sa_namespace
    annotations = {
      "eks.amazonaws.com/role-arn" = aws_iam_role.upload_service.arn
    }
  }

  depends_on = [kubernetes_namespace.irsa]
}


### service account for auth-service

resource "aws_iam_role" "auth_service" {
  name = var.auth_service_iam_role_name
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
          "${aws_iam_openid_connect_provider.this.url}:sub" = "system:serviceaccount:${var.sa_namespace}:${var.auth_service_sa_name}",
          "${aws_iam_openid_connect_provider.this.url}:aud" = "sts.amazonaws.com"
        }
      }
    }]
  })

  tags = var.stress_app_tags
}


locals{
  auth_service_actions = [
          "sns:Publish"
    ]
} 

resource "aws_iam_role_policy" "auth_service" {
  name = var.auth_service_policy_name
  role = aws_iam_role.auth_service.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action   = local.auth_service_actions
      Resource = aws_sns_topic.stress_app.arn
    }]
  })
}

resource "kubernetes_service_account" "auth_service" {
  metadata {
    name      = var.auth_service_sa_name
    namespace = var.sa_namespace
    annotations = {
      "eks.amazonaws.com/role-arn" = aws_iam_role.auth_service.arn
    }
  }

  depends_on = [kubernetes_namespace.irsa]
}

