data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids" "main" {
  vpc_id = local.vpc_id
}