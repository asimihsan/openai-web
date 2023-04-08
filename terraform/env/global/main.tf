provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "terraform_backend" {
  bucket = var.backend_bucket_name
}

resource "aws_s3_bucket_public_access_block" "terraform_backend" {
  bucket = aws_s3_bucket.terraform_backend.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_acl" "terraform_backend" {
  bucket = aws_s3_bucket.terraform_backend.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "terraform_backend" {
  bucket = aws_s3_bucket.terraform_backend.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = var.backend_dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}