variable "aws_region" {
  description = "The AWS region to create things in."
  default     = "us-west-1"
}
variable "env" {
  name = "dev"
}
variable "eb_app_name" {
  name = "birthday-api"
  description = "App Name"
}

variable "eb_app_env" {
  name = "birthday-api-env"
}
variable "vpc" {
  name = "vpc-xxxxx"
}
variable "subnets" {
  name = "subnet-xxxxx"
}
variable "solution_stack_name" {
  name = "Python 2.7 running on 64bit Amazon Linux"
}
variable "artifact" {
  name = "birthday-service.zip"
}
variable "version" {
  name = "v1"
}
variable "s3_bucket" {
  name = "prod-birthday-service.bucket"
}