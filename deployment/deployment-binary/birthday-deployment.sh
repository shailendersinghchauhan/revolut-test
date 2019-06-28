#!/bin/bash
######################################################
# Name: birthday-deployment.sh
# Purpose: Deploys or switch test env with live env on AWS EB service
# Author: Shailender
# Version: 1.0
# How to Use:
#------------------
# NOTE: ---Call it from Jenkins and provide values for -blue and -green
# ---- TEST TO LIVE
# Usage: .\birthday-deployment.sh -blue BLUE-ENV -green GREEN-ENV
#
# ---- LIVE TO TEST
# Usage: .\birthday-deployment.sh -blue GREEN-ENV -green BLUE-ENV
#
######################################################
deploy_usage()
{
  echo "-------------------------------------------------------"
  echo "Usage:"
  echo "-blue <EB blue env name>"
  echo "-green <EB green env name>"
  1>&2; exit 1;
}

deploy_service()
{
while getopts "blue:green:" o; do
  case "${o}" in
    blue)
      blue=${OPTARG}
     ;;
    green)
      green=${OPTARG}
      ;;
    *)
      deploy_usage
      ;;
  esac
done
shift $((OPTIND-1))

echo "******** Starting Birthday Deployment script **************"
GREEN_ENV=$green
BLUE_ENV=$blue

echo "Switching test environment[$BLUE_ENV] with LIVE environment[$GREEN_ENV]..."

eb swap $BLUE_ENV --destination_name $GREEN_ENV

echo "********** Successfully Completed **********"
}

###############Call Deployment##################
deploy_service