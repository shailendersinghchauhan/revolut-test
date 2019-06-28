#Data Resources
provider "aws" {
  region = "us-west-2"
}

module "eb-setup" {
  source = "../application-library/"
  env = ${var.env}
  vpc = ${var.vpc}
  eb_app_name = ${var.eb_app_name}
  eb_app_env = ${var.eb_app_name}
  version = ${var.version}
  s3_bucket = ${var.s4_bucket}
  solution_stack_name = ${var.solution_stack_name}
  artifact = ${var.artifact}
  subnets = ${var.subnets}
}