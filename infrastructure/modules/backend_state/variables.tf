variable "bucket_name" {
  type = string
}

variable "terraform_principal_arns" {
  type    = list(string)
  default = []
}

variable "tags" {
  type    = map(string)
  default = {}
}
