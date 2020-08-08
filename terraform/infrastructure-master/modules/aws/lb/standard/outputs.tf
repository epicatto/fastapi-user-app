output "arn" {
  value = aws_lb.main.arn
}

output "dns_name" {
  value = aws_lb.main.dns_name
}

output "zone_id" {
  value = aws_lb.main.zone_id
}

output "security_groups" {
  value = aws_lb.main.security_groups
}

output "subnets" {
  value = aws_lb.main.subnets
}

output "target_group_arn" {
  value = aws_lb_target_group.main.arn
}