module "main" {
  source = "../../"

  ecr_repository_url = var.ecr_repository_url
  image_tag          = var.image_tag
}

provider "aws" {
  region = "us-west-2"
}
