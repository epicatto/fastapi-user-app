variable "name" {
  type = string
}

variable "environment" {
  type = string
}
variable "vpc_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "certificate_arn" {
  type = string
}

### OPTIONAL

variable "security_group_names" {
  type = list(string)
  default = [
    "allow_http_from_everywhere",
    "allow_http_to_intranet"]
}

variable "internal" {
  type = bool
  default = true
}

variable "group_port" {
  type = string
  default = "80"
}

variable "health_check" {
  type = object({
    enabled = bool
    interval = number
    path = string
    port = string
    protocol = string
    timeout = number
    healthy_threshold = number
    unhealthy_threshold = number
    matcher = string
  })

  default = null
}

variable "module_depends_on" {
  # the value doesn't matter; we're just using this variable
  # to propagate dependencies.
  type = any
  default = []
}

variable "target_type" {
  type = string
  default = "instance"
}