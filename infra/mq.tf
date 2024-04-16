### rabbitmq 

resource "aws_security_group" "rabbitmq_sg" {
  name        = "rabbitmq-sg"
  description = "Security group for RabbitMQ"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description = "Allow AMQP (5672) access"
    from_port   = 5672
    to_port     = 5672
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # e.g., ["10.0.0.0/16"] or allow only app nodes
  }

  ingress {
    description = "Allow management UI (15672) access"
    from_port   = 15672
    to_port     = 15672
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Replace with your IP
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rabbitmq-sg"
  }
}


resource "aws_mq_broker" "rabbitmq_broker" {
  broker_name         = var.rabbitmq_broker_name
  engine_type         = "RabbitMQ"
  engine_version      = var.rabbitmq_engine_version
  host_instance_type  = var.rabbitmq_host_instance_type
  deployment_mode     = var.rabbitmq_deployment_mode
  #security_groups  = [aws_security_group.rabbitmq_sg.id]
  subnet_ids = [
    module.vpc.public_subnets[0]   # just for now putting in public 
  ]
  publicly_accessible = true
  configuration {
    id       = aws_mq_configuration.rabbitmq_broker_config.id
    revision = aws_mq_configuration.rabbitmq_broker_config.latest_revision
  }
  
  user {
    username = var.rabbit_mq_username
    password = var.rabbit_mq_password
  }

  auto_minor_version_upgrade = true
  maintenance_window_start_time {
    day_of_week = "MONDAY"
    time_of_day = "18:00"
    time_zone   = "UTC"
  }

  apply_immediately = true
}


resource "aws_mq_configuration" "rabbitmq_broker_config" {
  description    = "RabbitMQ config"
  name           = var.rabbitmq_broker_name
  engine_type    = "RabbitMQ"
  engine_version = var.rabbitmq_engine_version
  data           = <<DATA
# Default RabbitMQ delivery acknowledgement timeout is 30 minutes in milliseconds
consumer_timeout = 1800000
DATA
}