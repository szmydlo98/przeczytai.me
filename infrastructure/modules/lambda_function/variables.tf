variable "function_name" {
  type = string
}

variable "description" {
  type    = string
  default = null
}

variable "handler" {
  type    = string
  default = null
}

variable "runtime" {
  type    = string
  default = "python3.13"
}

variable "filename" {
  type    = string
  default = null
}

variable "source_code_hash" {
  type    = string
  default = null
}

variable "package_type" {
  type    = string
  default = "Zip"

  validation {
    condition     = contains(["Zip", "Image"], var.package_type)
    error_message = "package_type must be either Zip or Image."
  }
}

variable "image_uri" {
  type    = string
  default = null
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
