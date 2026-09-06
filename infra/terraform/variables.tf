variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment name"
  type        = string
  default     = "staging"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t4g.medium"
}

variable "anthropic_api_key" {
  description = "Anthropic API key, injected via secrets manager in real deployments"
  type        = string
  sensitive   = true
}
