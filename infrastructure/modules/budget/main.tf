resource "aws_ce_cost_allocation_tag" "project" {
  count = var.activate_cost_allocation_tag ? 1 : 0

  tag_key = var.project_tag_key
  status  = "Active"
}

resource "aws_budgets_budget" "project" {
  account_id   = var.account_id
  name         = var.name
  budget_type  = "COST"
  limit_amount = tostring(var.limit_amount_usd)
  limit_unit   = "USD"
  time_unit    = "MONTHLY"
  tags         = merge(var.tags, { Name = var.name })

  dynamic "cost_filter" {
    for_each = var.filter_by_project_tag ? [1] : []

    content {
      name   = "TagKeyValue"
      values = [format("user:%s$%s", var.project_tag_key, var.project_tag_value)]
    }
  }

  dynamic "notification" {
    for_each = toset(var.notification_thresholds)

    content {
      comparison_operator        = "GREATER_THAN"
      notification_type          = "ACTUAL"
      threshold                  = notification.value
      threshold_type             = "PERCENTAGE"
      subscriber_email_addresses = var.subscriber_email_addresses
    }
  }

  depends_on = [aws_ce_cost_allocation_tag.project]
}
