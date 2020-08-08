resource "aws_ecs_cluster" "main" {
  name = "${var.app_name}-${var.environment}"

  tags = {
    Project = var.app_name
    Stage = var.environment
  }
}