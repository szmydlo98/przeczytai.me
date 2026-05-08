output "state_bucket_name" {
  value = module.backend_state.bucket_name
}

output "lock_table_name" {
  value = module.backend_state.lock_table_name
}

output "terraform_principal_arns" {
  value = module.backend_state.terraform_principal_arns
}
