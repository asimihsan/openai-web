resource "aws_api_gateway_rest_api" "websocket_chat" {
  name        = "doc-example-websocket-chat"
  description = "API Gateway for WebSocket chat example"
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "websocket_chat_resource" {
  rest_api_id = aws_api_gateway_rest_api.websocket_chat.id
  parent_id   = aws_api_gateway_rest_api.websocket_chat.root_resource_id
  path_part   = "websocket"
}

resource "aws_api_gateway_method" "websocket_chat_method" {
  rest_api_id   = aws_api_gateway_rest_api.websocket_chat.id
  resource_id   = aws_api_gateway_resource.websocket_chat_resource.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "websocket_chat_integration" {
  rest_api_id             = aws_api_gateway_rest_api.websocket_chat.id
  resource_id             = aws_api_gateway_resource.websocket_chat_resource.id
  http_method             = aws_api_gateway_method.websocket_chat_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${var.lambda_arn}/invocations"
}

resource "aws_api_gateway_deployment" "websocket_chat_deployment" {
  depends_on  = [aws_api_gateway_integration.websocket_chat_integration]
  rest_api_id = aws_api_gateway_rest_api.websocket_chat.id
  stage_name  = "prod"
}

resource "aws_lambda_permission" "apigateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_arn
  principal     = "apigateway.amazonaws.com"

  source_arn = "arn:aws:execute-api:${var.region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.websocket_chat.id}/*/*"
}

data "aws_caller_identity" "current" {}