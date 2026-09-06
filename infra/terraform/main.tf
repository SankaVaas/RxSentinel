terraform {
  required_version = ">= 1.7"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# NOTE: this is a structural starting point, not a deploy-ready config.
# See ecs.tf / rds.tf for the ECS cluster + RDS instance definitions.
# A production rollout should also add: VPC + private subnets, a secrets
# manager entry for ANTHROPIC_API_KEY (never a plain tfvars value), an ALB
# with TLS termination, and CloudWatch alarms on the escalation-queue depth.
