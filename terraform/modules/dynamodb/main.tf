resource "aws_dynamodb_table" "websocket_chat" {
  name         = "doc-example-websocket-chat"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "connection_id"

  attribute {
    name = "connection_id"
    type = "S"
  }

  lifecycle {
    prevent_destroy = false
  }
}
