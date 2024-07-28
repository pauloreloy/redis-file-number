
provider "aws" {
  region = "us-east-1"
}

variable "subnet_ids" {
  description = "List of subnet IDs"
  type        = list(string)
  default     = ["subnet-4436c932", "subnet-fd5647a4"]
}
variable "vpc_id" {
  description = "VPC ID"
  type        = string
  default     = "vpc-b23cbad6"
}

resource "aws_security_group" "redis_sg" {
  vpc_id = var.vpc_id
  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "redis_sg"
  }
}

resource "aws_elasticache_serverless_cache" "redis_data" {
  engine = "redis"
  name   = "data"
  cache_usage_limits {
    data_storage {
      maximum = 1
      unit    = "GB"
    }
    ecpu_per_second {
      maximum = 10000
    }
  }
  description              = "Data Server"
  #kms_key_id               = aws_kms_key.test.arn
  major_engine_version     = "7"
  security_group_ids       = [aws_security_group.redis_sg.id]
  subnet_ids               = var.subnet_ids
}