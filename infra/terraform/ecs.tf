resource "aws_ecs_cluster" "rxsentinel" {
  name = "rxsentinel-${var.environment}"
}

# Task definitions for backend/worker/frontend, an ALB, target groups, and
# service definitions are intentionally left as a follow-up once the VPC
# topology (main.tf) is decided — wiring these before that is a networking
# guess, not an architecture decision.
