output "api_base_url" {
  value = module.http_api.api_endpoint
}

output "api_lambda_function_name" {
  value = module.api_lambda.function_name
}

output "processor_lambda_function_name" {
  value = module.processor_lambda.function_name
}

output "processor_ecr_repository_url" {
  value = aws_ecr_repository.processor.repository_url
}

output "metadata_table_name" {
  value = module.storage.metadata_table_name
}

output "files_bucket_name" {
  value = module.storage.files_bucket_name
}

output "budget_name" {
  value = module.budget.budget_name
}
