output "dynamodb_table_name" {
  value = module.dynamodb.table_name
}

output "lambda_function_name" {
  value = module.lambda.function_name
}

output "api_gateway_id" {
  value = module.apigateway.api_gateway_id
}
