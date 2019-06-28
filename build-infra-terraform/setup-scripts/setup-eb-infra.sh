#!/bin/bash
##################################
# Name: setup-eb-infra.sh
# Purpose: Build Terraform Infra on AWS
# Author: Shailender
##################################
echo "Performing Terraform steps for deployment"

ENV="blue"

terraform init ../$ENV/
terraform plan ../$ENV/
terraform deploy ../$ENV/

echo "***** Teraforming Done ********"