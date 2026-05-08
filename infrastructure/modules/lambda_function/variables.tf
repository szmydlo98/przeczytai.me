variable "function_name" {
  type = string
}

variable "description" {
  type    = string
  default = null
}

variable "handler" {
  type = string
}

variable "runtime" {
  type    = string
  default = "python3.13"
}

variable "filename" {
  type = string
}

variable "source_code_hash" {
  type = string
}

variable "timeout" {
  type = number
}

variable "memory_size" {
  type = number
}

variable "environment_variables" {
  type    = map(string)
  default = {}
}

variable "policy_statements" {
  type = list(object({
    sid       = string
    actions   = list(string)
    resources = list(string)
  }))
  default = []
}

variable "log_retention_days" {
  type    = number
  default = 14
}

variable "tags" {
  type    = map(string)
  default = {}
}
