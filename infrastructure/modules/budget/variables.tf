variable "account_id" {
  type = string
}

variable "name" {
  type = string
}

variable "limit_amount_usd" {
  type = number
}

variable "subscriber_email_addresses" {
  type = set(string)
}

variable "notification_thresholds" {
  type    = list(number)
  default = [50, 80, 95]
}

variable "project_tag_key" {
  type    = string
  default = "Project"
}

variable "project_tag_value" {
  type = string
}

variable "filter_by_project_tag" {
  type    = bool
  default = true
}

variable "activate_cost_allocation_tag" {
  type    = bool
  default = true
}

variable "tags" {
  type    = map(string)
  default = {}
}
