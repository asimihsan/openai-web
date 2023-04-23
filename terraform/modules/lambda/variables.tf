variable "ecr_repository_url" {
  description = "The URL of the ECR repository"
}

variable "image_tag" {
  description = "The tag of the image to deploy"
}

variable "dynamodb_table_name" {
  description = "The name of the DynamoDB table"
}

variable "dynamodb_table_arn" {
  description = "The ARN of the DynamoDB table"
}
