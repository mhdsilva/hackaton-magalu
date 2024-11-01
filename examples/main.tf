provider "aws" {
    region = "us-east-1"
}

variable "bucket_name" {

}

resource "aws_s3_bucket" "static_site_bucket" {
    bucket = "static-site-${var.bucket_name}"

    website {
        index_document = "index.html"
        error_document = "404.html"
    }

    tags = {
        Name = "Static Site Bucket"
        Enviroment = "Production"
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
