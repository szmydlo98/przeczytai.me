terraform {
  backend "s3" {
    bucket         = "przeczytai-me-tfstate-638175212741-eu-west-1"
    key            = "environments/dev/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "przeczytai-me-tf-locks"
    encrypt        = true
    use_lockfile   = true
  }
}
