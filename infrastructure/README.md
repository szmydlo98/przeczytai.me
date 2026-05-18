# Terraform

This directory contains the AWS infrastructure for `przeczytai.me`.

## Layout

- `modules/` contains reusable resource modules.
- `environments/bootstrap/` creates the Terraform state S3 bucket. State locking uses the S3 backend lockfile.
- `environments/dev/` creates the dev application stack.

## Bootstrap State

Run bootstrap first with local state:

```bash
terraform -chdir=infrastructure/environments/bootstrap init
terraform -chdir=infrastructure/environments/bootstrap apply
```

Bootstrap creates:

- S3 bucket: `przeczytai-me-tfstate-638175212741-eu-west-1`

By default, the state bucket policy restricts state access to the AWS caller that applies bootstrap. To use a dedicated Terraform role instead, pass `terraform_principal_arns`.

## Dev

Create a local tfvars file from the example:

```bash
cp infrastructure/environments/dev/terraform.tfvars.example infrastructure/environments/dev/terraform.tfvars
terraform -chdir=infrastructure/environments/dev init
terraform -chdir=infrastructure/environments/dev apply
```

The dev backend stores state at `environments/dev/terraform.tfstate`.

The processor Lambda is deployed from an ECR image. On the first deploy, create
the repository before pushing the image:

```bash
terraform -chdir=infrastructure/environments/dev apply -target=aws_ecr_repository.processor
backend/scripts/build-push-processor-image.sh
terraform -chdir=infrastructure/environments/dev apply
```

## Validation

```bash
terraform -chdir=infrastructure/environments/bootstrap init -backend=false
terraform -chdir=infrastructure/environments/bootstrap validate
terraform -chdir=infrastructure/environments/dev init -backend=false
terraform -chdir=infrastructure/environments/dev validate
```
