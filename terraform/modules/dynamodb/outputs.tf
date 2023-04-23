output "table_name" {
  value = aws_dynamodb_table.websocket_chat.name
}

output "table_arn" {
  value = aws_dynamodb_table.websocket_chat.arn
}
