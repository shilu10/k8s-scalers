output "kubernetes_endpoint" {
  value = aws_eks_cluster.this.endpoint
}

output "kubernetes_id" {
  value = aws_eks_cluster.this.id
}

output "kubernetes_arn" {
  value = aws_eks_cluster.this.arn
}

output "kubernetes_status" {
  value = aws_eks_cluster.this.status
}

output "kubernetes_ca" {
  value = aws_eks_cluster.this.certificate_authority
}

output "kubernets_ng_resources" {
  value = aws_eks_node_group.this.resources
}

output "kubernetes_ng_status" {
  value = aws_eks_node_group.this.status
}

output "rds_endpoint" {
  value = aws_db_instance.mysql.endpoint
}

output "ecr_repos_url" {
  value = { for repo_name, repo in aws_ecr_repository.repos : repo_name => repo.repository_url }
}

output "lambdas_arn" {
  value = { for lambda_name, lambda in aws_lambda_function.stress_app : lambda_name => lambda.arn }
}

output "sns_topic_arn" {
  value = aws_sns_topic.stress_app.arn
}

output "redis_instance_ip" {
  value = aws_instance.redis.private_ip
}

output "mongodb_uri" {
  value = mongodbatlas_cluster.cluster.mongo_uri
  sensitive = true
}

output "rabbitmq_url" {
  value = cloudamqp_instance.instance.url
  sensitive = true
}