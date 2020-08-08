data "aws_security_group" "main" {
  count = length(var.names)

  filter {
    name = "group-name"
    values = [
      var.names[count.index]]
  }

  depends_on = [
    var.module_depends_on]
}
