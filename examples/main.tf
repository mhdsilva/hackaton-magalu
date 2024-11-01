provider "aws" {
  region = "us-east-1"
}

variable "aws_access_key" {
  description = "Chave de acesso da AWS."
}

variable "aws_secret_key" {
  description = "Chave secreta da AWS."
}

variable "region" {
  description = "Região da AWS."
  default     = "us-east-1"
}

variable "instance_type" {
  description = "Tipo de instância EC2."
  default     = "t2.micro"
}

variable "ami" {
  description = "ID da AMI para a instância EC2."
}

variable "s3_bucket_name" {
  description = "Nome do bucket S3."
  default     = "meu-bucket-app"
}

resource "aws_s3_bucket" "static_site_bucket" {
  bucket = "static-site-${var.s3_bucket_name}"

  website {
    index_document = "index.html"
    error_document = "404.html"
  }

  tags = {
    Name        = "Static Site Bucket"
    Environment = "Production"
  }
}

resource "aws_instance" "database_server" {
  ami                         = "ami-0def12345abc67890"
  instance_type               = "t2.medium"
  key_name                    = "db-key"
  associate_public_ip_address = false
  subnet_id                   = "subnet-87654321"
  vpc_security_group_ids      = ["sg-87654321"]
  tags = {
    Name = "DatabaseServer"
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

data "aws_instance" "existing_instance" {
  instance_id = aws_instance.database_server.id
}

data "aws_s3_bucket" "existing_bucket" {
  bucket = aws_s3_bucket.static_site_bucket.bucket
}

output "vm_images" {
  value = data.aws_ami.ubuntu.images
}

output "vm_instances" {
  value = data.aws_instance.existing_instance
}

output "vm_bucket" {
  value = data.aws_s3_bucket.existing_bucket
}
