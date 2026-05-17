output "bucket_name" {
  value = aws_s3_bucket.state.bucket
}

output "bucket_arn" {
  value = aws_s3_bucket.state.arn
}

output "terraform_principal_arns" {
  value = local.terraform_principal_arns
}
