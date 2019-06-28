provider "aws" {
  region = "${var.aws_region}"
}

resource "aws_elastic_beanstalk_application" "eb-app-name" {
  name        = "${var.eb_app_name}-${var.env}"
  description = "Single live Green environment"
}

resource "aws_elastic_beanstalk_environment" "eb-app-env" {
  name                = "${var.eb_app_env}-${var.env}"
  application         = "${aws_elastic_beanstalk_application.eb-app-name.name}"
  solution_stack_name = "${var.solution_stack_name}"

  setting {
    namespace = "aws:ec2:vpc"
    name      = "VPCId"
    value     = "${var.vpc}"
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "Subnets"
    value     = "${var.subnets}"
  }
}
resource "aws_elastic_beanstalk_configuration_template" "eb-app-template" {
  name                = "prod-birthday-service-template-config"
  application         = "${aws_elastic_beanstalk_application.eb-app-name.name}"
  solution_stack_name = "${var.solution_stack_name}"
}
resource "aws_s3_bucket" "default" {
  bucket ="${var.s3_bucket}"
}

resource "aws_s3_bucket_object" "default" {
  bucket = "${aws_s3_bucket.default.id}"
  key    = "../../deployment/artifact/${var.env}-birthday-service-${var.env}.zip"
  source = "${var.env}-birthday-service-${var.version}.zip"
}

resource "aws_elastic_beanstalk_application_version" "default" {
  name        = "prod-birthday-service=version-label"
  application = "green-prod-birthday-service-app"
  description = "Birthday application version created by terraform"
  bucket      = "${aws_s3_bucket.default.id}"
  key         = "${aws_s3_bucket_object.default.id}"
}