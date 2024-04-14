### RDS Setup (for mysql) accessed and used by auth-service for storing users information and token revocation


resource "aws_db_subnet_group" "default" {
  name       = var.mysql_db_subnet_group_name
  subnet_ids = module.vpc.private_subnets
  tags       = var.stress_app_tags
}


resource "aws_security_group" "rds_mysql_sg" {
  name        = var.rds_sg_name
  description = "Allow Redis access from EKS worker nodes"
  vpc_id      = module.vpc.vpc_id

  tags = var.stress_app_tags
}


# Allow Redis access from EKS node SG
resource "aws_security_group_rule" "mysql_from_eks" {
  type                     = "ingress"
  from_port                = 3306
  to_port                  = 3306
  protocol                 = "tcp"
  security_group_id        = aws_security_group.rds_mysql_sg.id
  source_security_group_id = aws_security_group.eks_nodes_sg.id
}


resource "aws_db_instance" "mysql" {
  identifier             = var.upload_service_db
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = var.mysqldb_instance_class
  allocated_storage      = var.mysql_allocated_storage
  db_name                = var.mysqldb_name
  username               = var.mysqldb_username
  password               = var.mysqldb_password
  db_subnet_group_name   = aws_db_subnet_group.default.name
  vpc_security_group_ids = [aws_security_group.rds_mysql_sg.id]
  skip_final_snapshot    = true
  publicly_accessible    = false
  storage_encrypted      = true
  multi_az               = false

  tags = var.stress_app_tags
}

