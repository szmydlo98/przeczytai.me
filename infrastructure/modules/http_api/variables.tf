variable "api_name" {
  type = string
}

variable "lambda_function_name" {
  type = string
}

variable "lambda_invoke_arn" {
  type = string
}

variable "jwt_issuer" {
  type = string
}

variable "jwt_audiences" {
  type = list(string)
}

variable "allowed_origins" {
  type = list(string)
}

variable "access_log_retention_days" {
  type    = number
  default = 14
}

variable "tags" {
  type    = map(string)
  default = {}
}
