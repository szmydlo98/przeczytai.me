data "aws_caller_identity" "current" {}

locals {
  state_bucket_name = "${var.project_slug}-tfstate-${var.aws_account_id}-${var.aws_region}"
  lock_table_name   = "${var.project_slug}-tf-locks"

  common_tags = {
    Project     = var.project_name
    Environment = "bootstrap"
    ManagedBy   = "terraform"
  }
}

module "backend_state" {
  source = "../../modules/backend_state"

  bucket_name              = local.state_bucket_name
  lock_table_name          = local.lock_table_name
  terraform_principal_arns = length(var.terraform_principal_arns) > 0 ? var.terraform_principal_arns : [data.aws_caller_identity.current.arn]
  tags                     = local.common_tags
}
