provider "aws" {
  region = var.aws_region
}

module "dynamodb" {
  source = "./modules/dynamodb"
}

module "lambda" {
  source              = "./modules/lambda"
  dynamodb_table_name = module.dynamodb.table_name
  dynamodb_table_arn  = module.dynamodb.table_arn
}

module "apigateway" {
  source     = "./modules/apigateway"
  region     = var.aws_region
  lambda_arn = module.lambda.lambda_arn
}
