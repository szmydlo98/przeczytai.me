variable "aws_account_id" {
  type    = string
  default = "638175212741"
}

variable "aws_region" {
  type    = string
  default = "eu-west-1"
}

variable "project_name" {
  type    = string
  default = "przeczytai.me"
}

variable "project_slug" {
  type    = string
  default = "przeczytai-me"
}

variable "terraform_principal_arns" {
  type    = list(string)
  default = []
}
