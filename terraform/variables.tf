variable "aws_access_key" {
  type = string
  description = "AWS access key"
}
variable "aws_secret_key" {
  type = string
  description = "AWS secret key"
}
variable "aws_account_id" {
  type = string
  description = "AWS account ID"
}
variable "aws_region" {
  type = string
  description = "AWS region e.g. us-east-1 (Please specify a region supported by the Fargate launch type)"
}
variable "app_name" {
  type = string
  description = "Prefix to be used in the naming of some of the created AWS resources e.g. demo-webapp"
}
variable "ecr_name" {
  type = string
  description = "Elastic Container Registry name."
}
variable "img_tag" {
  type = string
  description = "Docker image tag."
}
variable "environment" {
  type = string
  description = "Environment where the application will be deployed."
}
variable "app_db_schema" {
  type = string
  description = "Data base schema used by the application (e.g. postgres)."
}
variable "app_db_server" {
  type = string
  description = "Database server name."
}
variable "app_db_user" {
  type = string
  description = "Database user"
}
variable "app_db_password" {
  type = string
  description = "Database user password."
}
variable "app_db_name" {
  type = string
  description = "Database name."
}
variable "app_db_port" {
  type = string
  description = "Database port."
}