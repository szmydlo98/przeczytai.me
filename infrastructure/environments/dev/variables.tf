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

variable "environment" {
  type    = string
  default = "dev"
}

variable "allowed_origins" {
  type    = list(string)
  default = ["http://localhost:3000"]
}

variable "max_text_chars" {
  type    = number
  default = 100000
}

variable "api_lambda_timeout_seconds" {
  type    = number
  default = 20
}

variable "api_lambda_memory_size" {
  type    = number
  default = 256
}

variable "processor_lambda_timeout_seconds" {
  type    = number
  default = 30
}

variable "processor_lambda_memory_size" {
  type    = number
  default = 256
}

variable "budget_limit_usd" {
  type    = number
  default = 8
}

variable "budget_subscriber_email_addresses" {
  type    = set(string)
  default = ["leski.jn@gmail.com"]
}

variable "activate_project_cost_allocation_tag" {
  type    = bool
  default = true
}
