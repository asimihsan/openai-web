variable "aws_region" {
  description = "AWS region for the resources"
  default     = "us-west-2"
}

variable "backend_bucket_name" {
  description = "The name of the S3 bucket for the Terraform backend"
}

variable "backend_dynamodb_table_name" {
  description = "The name of the DynamoDB table for the Terraform backend"
}
