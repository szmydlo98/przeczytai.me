output "files_bucket_name" {
  value = aws_s3_bucket.files.bucket
}

output "files_bucket_arn" {
  value = aws_s3_bucket.files.arn
}

output "metadata_table_name" {
  value = aws_dynamodb_table.metadata.name
}

output "metadata_table_arn" {
  value = aws_dynamodb_table.metadata.arn
}
