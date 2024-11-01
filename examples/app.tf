provider "aws" {
  region = "us-west-1"
}

variable "aws_access_key" {
  description = "Chave de acesso da AWS."
}

variable "aws_secret_key" {
  description = "Chave secreta da AWS."
}

variable "region" {
  description = "Região da AWS."
  default     = "us-west-1"
}

variable "instance_type" {
  description = "Tipo de instância EC2."
  default     = "t2.small"
}

variable "ami" {
  description = "ID da AMI para a instância EC2."
}

variable "s3_bucket_name" {
  description = "Nome do bucket S3."
  default     = "meu-bucket-webapp"
}

resource "aws_security_group" "web_sg" {
  name        = "web-security-group"
  description = "Security group for web servers"

  ingress {
    from_port   = 80
    to_port     = 80
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
    Name = "WebSG"
  }
}

resource "aws_instance" "web_server" {
  ami                         = "ami-0abc12345def67890"
  instance_type               = "t2.small"
  key_name                    = "web-key"
  associate_public_ip_address = true
  subnet_id                   = "subnet-12345678"
  vpc_security_group_ids      = ["sg-12345678"]
  tags = {
    Name = "WebServer"
  }
}

data "aws_ami" "nginx" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["nginx/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

data "aws_security_group" "existing_sg" {
  id = aws_security_group.web_sg.id
}

output "web_server_status" {
  value = data.aws_instance.web_server.state
}

output "web_server_image" {
  value = data.aws_ami.nginx.id
}

output "web_security_group" {
  value = data.aws_security_group.existing_sg.name
}
