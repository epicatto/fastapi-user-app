resource "aws_cloudwatch_log_group" "lg" {
  name = "/${var.resource}/${var.app_name}-${var.environment}"
  retention_in_days = var.retention_in_days

  tags = {
    Project = var.app_name
    Stage = var.environment
  }
}