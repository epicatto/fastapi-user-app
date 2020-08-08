variable "names" {
  description = "A list of security groups names which IDs to lookup."
  default = []
}

variable "module_depends_on" {
  # the value doesn't matter; we're just using this variable
  # to propagate dependencies.
  type = any
  default = []
}
