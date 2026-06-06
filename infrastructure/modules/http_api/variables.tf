variable "api_name" {
  type = string
}

variable "lambda_function_name" {
  type = string
}

variable "lambda_invoke_arn" {
  type = string
}

variable "allowed_origins" {
  type = list(string)
}

variable "clerk_jwt_issuer" {
  type        = string
  description = "Clerk issuer URL for JWT validation."
}

variable "clerk_jwt_audience" {
  type        = string
  description = "Expected audience claim for Clerk JWTs accepted by this API."
}

variable "access_log_retention_days" {
  type    = number
  default = 14
}

variable "tags" {
  type    = map(string)
  default = {}
}
