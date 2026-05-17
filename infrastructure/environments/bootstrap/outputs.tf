output "state_bucket_name" {
  value = module.backend_state.bucket_name
}

output "terraform_principal_arns" {
  value = module.backend_state.terraform_principal_arns
}
