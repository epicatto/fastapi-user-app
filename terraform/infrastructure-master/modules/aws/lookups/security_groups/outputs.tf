output "ids" {
  description = "A list of security group ids"
  value = data.aws_security_group.main.*.id
}
