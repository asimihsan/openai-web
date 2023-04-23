variable "aws_region" {
  description = "AWS region for the resources"
  default     = "us-west-2"
}

variable "ecr_repository_url" {
  description = "ECR repository URL"
}

variable "image_tag" {
  description = "Image tag"
}
