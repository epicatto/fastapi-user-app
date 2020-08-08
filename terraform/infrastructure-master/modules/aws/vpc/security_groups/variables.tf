variable "vpc_id" {
  type = string
}

variable "intranet_cidr_blocks" {
  type = list(string)
  default = []
}

variable "vpc_name" {
  type = string
  default = "default"
}

