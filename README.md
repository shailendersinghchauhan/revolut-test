# revolut-test

**build-infra-terraform** - It contains terraform code to build AWS Elastic Beanstalks infra and deploys first python web package developed in Flask
It contains application-library that has eb-setup.tf that is a terraform library that is callable from Modules mentioned in environment specific folder here like blue  / green
setup-scripts - It contains basis bash script that has terraform init/plan/deploy steps

**deployment** - It contains artifact and deployment-binary where artifact contains application.py and requirements.txt dependency modules for python that EB will use to install packages.
deployment-binary - It contains bash script that will swtich/swap blue envrionment with live Green environment after successfully 'eb deploy' command on blue/test Environment.

**doc** - It contains deployment solution architecture diagram provided by AWS that can easily be implemented with proper CI/CD pipeline through Jenkins or similar CI/CD tool.

**NOTES by Shailender:**

_-Terraform code is not complete and tested but we are showing how we will be deploying AWS EB infra.

-Build and Deploy scripts are not tested due to time shortage as other wise we can follow many other best practices in such scripts like terraform version verificaiton using semver, backend configuration with S3 or other supported backends._

-application.py - contains actual birthday service code and we have to pass DB creds as global variable. In actual prod we should be using encrypted seprate config and then will read configs in python script.

**AWS EB INFRA SETUP:**

_./setup-eb-infra.sh_

**LIVE Deployment:**

._/birthday-deployment.sh -blue BLUE-BIRTHDAY-API -green GREEN-BIRTHDAY-API_


NOTE: Call this script from Jenkins or other CI/CD tool.

DEPLOYMENT INFO:
1. We could have used AWS ECS instead of Beanstalk as it can be deployed on existing cluster as other wise EB will deploy its own instances.
2. Even it can deployed as AWS Lambda but we have to setup AWS API Gateway for that but as of now for this test AWS Beanstalks looks simpler in normal cases.
