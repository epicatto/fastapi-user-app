resource "aws_ecr_repository" "app_repository" {
  name = "${var.app_name}-${var.environment}"
}