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