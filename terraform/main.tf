module "security-groups" {
  //  source                = "git@github.com:nexton-labs/infrastructure.git//modules/aws/vpc/security_groups"
  source = "./infrastructure-master/modules/aws/vpc/security_groups"
  vpc_id = local.vpc_id
}

module "lookup-security-groups" {
  //  source                = "git@github.com:nexton-labs/infrastructure.git//modules/aws/vpc/security_groups"
  source = "./infrastructure-master/modules/aws/lookups/security_groups"
  names = [
    "allow_http_from_everywhere",
    "allow_all_to_everywhere",
  ]
  module_depends_on = [
    module.security-groups]
}

module "ecs-cluster" {
  //  source      = "git@github.com:nexton-labs/infrastructure.git//modules/aws/ecs"
  source = "./infrastructure-master/modules/aws/ecs"
  app_name = local.app_name
  environment = local.environment
}

module "logs" {
  //  source            = "git@github.com:nexton-labs/infrastructure.git//modules/aws/cloudwatch"
  source = "./infrastructure-master/modules/aws/cloudwatch"
  app_name = local.app_name
  environment = local.environment
  resource = "ecs"
  retention_in_days = 7
}

module "ecs-lb" {
  //  source      = "git@github.com:nexton-labs/infrastructure.git//modules/aws/lb/standard"
  source = "./infrastructure-master/modules/aws/lb/standard"
  name = local.app_name
  environment = local.environment
  vpc_id = local.vpc_id
  subnet_ids = local.subnet_ids
  internal = false
  target_type = "ip"
  certificate_arn = local.certificate_arn
  health_check = {
    enabled = true
    interval = 30
    port = 80
    protocol = "HTTP"
    path = local.health_check_path
    timeout = 5
    healthy_threshold = 2
    unhealthy_threshold = 2
    matcher = "200"
  }
  module_depends_on = [
    module.security-groups.groups_from_everywhere,
    module.security-groups.groups_all_to_everywhere]
}

resource "aws_ecs_task_definition" "app-task" {
  family = join("-", [
    local.app_name,
    "task"])
  requires_compatibilities = [
    "FARGATE"]
  network_mode = "awsvpc"
  cpu = 256
  memory = 512
  container_definitions = "[${local.container_definition}]"
  execution_role_arn = module.ecs-cluster.execution_role_arn
}
resource "aws_ecs_service" "app-service" {
  lifecycle {
    ignore_changes = [
      desired_count,
    ]
  }
  name = "${local.app_name}-${local.environment}"
  cluster = module.ecs-cluster.id
  launch_type = "FARGATE"
  task_definition = aws_ecs_task_definition.app-task.arn
  desired_count = 1
  network_configuration {
    subnets = module.ecs-lb.subnets
    security_groups = module.lookup-security-groups.ids
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = module.ecs-lb.target_group_arn
    container_name = "${local.app_name}-${local.environment}"
    container_port = local.container_port
  }
  depends_on = [
    module.ecs-lb,
    aws_ecs_task_definition.app-task]
}

locals {
  app_name = var.app_name
  environment = var.environment
  default_region = var.aws_region
  cluster_name = join("-", [
    local.app_name,
    local.environment,
    "cluster"])
  container_port = 80
  vpc_id = data.aws_vpc.default.id
  subnet_ids = data.aws_subnet_ids.main.ids
  health_check_path = "/docs"
  certificate_arn = ""
  container_definition = jsonencode({
    "name" = "${local.app_name}-${local.environment}"
    "image" = format("%s.dkr.ecr.%s.amazonaws.com/%s:%s",
    var.aws_account_id, var.aws_region, var.ecr_name, var.img_tag)
    "essential" = true
    "networkMode" = "awsvpc"
    "environment" : [
      {
        name : "DB_SCHEME",
        value : var.app_db_schema
      },
      {
        name : "DB_SERVER",
        value : var.app_db_server
      },
      {
        name : "DB_USER",
        value : var.app_db_user
      },
      {
        name : "DB_PASSWORD",
        value : var.app_db_password
      },
      {
        name : "DB_NAME",
        value : var.app_db_name
      },
      {
        name : "DB_PORT",
        value : var.app_db_port
      }],
    "portMappings" = [
      {
        hostPort = 80,
        protocol = "tcp",
        containerPort = local.container_port
      }]
    "logConfiguration" = {
      "logDriver" = "awslogs",
      "options" = {
        "awslogs-group" = module.logs.log_group_name,
        "awslogs-region" = local.default_region,
        "awslogs-stream-prefix" = "ecs"
      }
    }
  })
}
