resource "aws_db_instance" "rxsentinel_postgres" {
  identifier              = "rxsentinel-${var.environment}"
  engine                  = "postgres"
  engine_version          = "16.3"
  instance_class          = var.db_instance_class
  allocated_storage       = 50
  db_name                 = "rxsentinel"
  username                = "rxsentinel"
  manage_master_user_password = true
  skip_final_snapshot     = var.environment != "production"
  backup_retention_period = var.environment == "production" ? 7 : 1

  # pgvector extension must be enabled post-creation via a parameter group
  # or a migration-time `CREATE EXTENSION IF NOT EXISTS vector;` (see
  # backend/alembic/versions/0001_initial_schema.py).
}
