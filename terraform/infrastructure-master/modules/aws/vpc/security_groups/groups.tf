##
# intranet {
##

# inbound {

resource "aws_security_group" "allow_all_from_intranet" {
  name = "allow_all_from_intranet"
  description = "Allow All from intranet"
  vpc_id = data.aws_vpc.main.id

  tags = {
    Name = "All Inbound From Intranet (${local.vpc_name})"
  }
}

resource "aws_security_group_rule" "allow_all_from_intranet" {
  type = "ingress"
  from_port = 0
  to_port = 0
  protocol = "all"
  cidr_blocks = local.intranet_cidr_blocks
  security_group_id = aws_security_group.allow_all_from_intranet.id
}

resource "aws_security_group" "allow_from_intranet" {
  for_each = local.groups

  name = "allow_${lower(each.key)}_from_intranet"
  description = "Allow ${each.key} from intranet"
  vpc_id = data.aws_vpc.main.id

  tags = {
    Name = "Inbound ${each.key} From Intranet (${local.vpc_name})"
  }
}

resource "aws_security_group_rule" "allow_from_intranet" {
  for_each = {
  for name, def in local.group_ports : def.key => def
  }

  type = "ingress"
  from_port = each.value.port
  to_port = each.value.port
  protocol = "tcp"
  cidr_blocks = local.intranet_cidr_blocks
  security_group_id = aws_security_group.allow_from_intranet[each.value.name].id
}

# inbound }

# outbound {

resource "aws_security_group" "allow_all_to_intranet" {
  name = "allow_all_to_intranet"
  description = "Allow All to intranet"
  vpc_id = data.aws_vpc.main.id

  tags = {
    Name = "All Inbound To Intranet (${local.vpc_name})"
  }
}

resource "aws_security_group_rule" "allow_all_to_intranet" {
  type = "ingress"
  from_port = 0
  to_port = 0
  protocol = "all"
  cidr_blocks = local.intranet_cidr_blocks
  security_group_id = aws_security_group.allow_all_to_intranet.id
}

resource "aws_security_group" "allow_to_intranet" {
  for_each = local.groups

  name = "allow_${lower(each.key)}_to_intranet"
  description = "Allow ${each.key} to intranet"
  vpc_id = data.aws_vpc.main.id

  tags = {
    Name = "Outbound ${each.key} To Intranet (${local.vpc_name})"
  }
}

resource "aws_security_group_rule" "allow_to_intranet" {
  for_each = {
  for name, def in local.group_ports : def.key => def
  }

  type = "egress"
  from_port = each.value.port
  to_port = each.value.port
  protocol = "tcp"
  cidr_blocks = local.intranet_cidr_blocks
  security_group_id = aws_security_group.allow_to_intranet[each.value.name].id
}

# outbound }

##
# intranet }
##

##
# everywhere {
##

# inbound {

resource "aws_security_group" "allow_from_everywhere" {
  for_each = {
  for name, def in local.groups : name => def
  if lookup(def, "public", false)
  }

  name = "allow_${lower(each.key)}_from_everywhere"
  description = "Allow ${each.key} from everywhere"
  vpc_id = data.aws_vpc.main.id

  tags = {
    Name = "Inbound ${each.key} From Everywhere (${local.vpc_name})"
  }
}

resource "aws_security_group_rule" "allow_from_everywhere" {
  for_each = {
  for name, def in local.group_ports : def.key => def
  if lookup(def, "public", false)
  }

  type = "ingress"
  from_port = each.value.port
  to_port = each.value.port
  protocol = "tcp"
  cidr_blocks = [
    "0.0.0.0/0"]
  security_group_id = aws_security_group.allow_from_everywhere[each.value.name].id
}

# inbound }

# outbound {

resource "aws_security_group" "allow_all_to_everywhere" {
  name = "allow_all_to_everywhere"
  description = "Allow all to everywhere"
  vpc_id = data.aws_vpc.main.id

  tags = {
    Name = "Outbound All To Everywhere (${local.vpc_name})"
  }
}

resource "aws_security_group_rule" "allow_all_to_everywhere" {
  type = "egress"
  description = "Allow all to everywhere"
  from_port = 0
  to_port = 0
  protocol = "-1"
  cidr_blocks = [
    "0.0.0.0/0"]
  security_group_id = aws_security_group.allow_all_to_everywhere.id
}

resource "aws_security_group" "allow_to_everywhere" {
  for_each = {
  for name, def in local.groups : name => def
  if lookup(def, "public", false)
  }

  name = "allow_${lower(each.key)}_to_everywhere"
  description = "Allow ${each.key} to everywhere"
  vpc_id = data.aws_vpc.main.id

  tags = {
    Name = "Outbound ${each.key} To Everywhere (${local.vpc_name})"
  }
}

resource "aws_security_group_rule" "allow_to_everywhere" {
  for_each = {
  for name, def in local.group_ports : def.key => def
  if lookup(def, "public", false)
  }

  type = "egress"
  from_port = each.value.port
  to_port = each.value.port
  protocol = "tcp"
  cidr_blocks = [
    "0.0.0.0/0"]
  security_group_id = aws_security_group.allow_to_everywhere[each.value.name].id
}

# outbound }

##
# everywhere }
##

