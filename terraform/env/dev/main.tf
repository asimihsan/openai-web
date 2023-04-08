module "main" {
  source = "../../"

  providers = {
    aws = aws
  }
}

provider "aws" {
  region = "us-west-2"
}
