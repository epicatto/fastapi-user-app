locals {
  default_health_check = {
    enabled = true
    interval = 30
    path = "/"
    port = var.group_port
    protocol = "HTTP"
    timeout = 5
    healthy_threshold = 3
    unhealthy_threshold = 3
    matcher = "200"
  }

  health_check = merge(local.default_health_check, {
    port = var.group_port
  }, coalesce(var.health_check, {}))
}
