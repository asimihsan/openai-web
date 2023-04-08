output "backend_bucket_name" {
  value = aws_s3_bucket.terraform_backend.bucket
}

output "backend_dynamodb_table_name" {
  value = aws_dynamodb_table.terraform_locks.name
}
