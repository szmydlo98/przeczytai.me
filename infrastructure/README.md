# Terraform

This directory contains the AWS infrastructure for `przeczytai.me`.

## Layout

- `modules/` contains reusable resource modules.
- `environments/bootstrap/` creates the Terraform state S3 bucket and DynamoDB lock table.
- `environments/dev/` creates the dev application stack.

## Bootstrap State

Run bootstrap first with local state:

```bash
terraform -chdir=infrastructure/environments/bootstrap init
terraform -chdir=infrastructure/environments/bootstrap apply
```

Bootstrap creates:

- S3 bucket: `przeczytai-me-tfstate-638175212741-eu-west-1`
- DynamoDB table: `przeczytai-me-tf-locks`

By default, the state bucket policy restricts state access to the AWS caller that applies bootstrap. To use a dedicated Terraform role instead, pass `terraform_principal_arns`.

## Dev

Create a local tfvars file from the example and set the Clerk issuer:

```bash
cp infrastructure/environments/dev/terraform.tfvars.example infrastructure/environments/dev/terraform.tfvars
terraform -chdir=infrastructure/environments/dev init
terraform -chdir=infrastructure/environments/dev apply
```

The dev backend stores state at `environments/dev/terraform.tfstate`.

## Validation

```bash
terraform -chdir=infrastructure/environments/bootstrap init -backend=false
terraform -chdir=infrastructure/environments/bootstrap validate
terraform -chdir=infrastructure/environments/dev init -backend=false
terraform -chdir=infrastructure/environments/dev validate
```
