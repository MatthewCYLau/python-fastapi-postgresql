resource "random_id" "db_name_suffix" {
  byte_length = 4
}

resource "google_sql_database_instance" "this" {
  name   = "python-fastapi-${random_id.db_name_suffix.hex}"
  region = var.region

  // public network settings
  settings {
    tier              = "db-f1-micro"
    availability_type = "REGIONAL"
    user_labels = {
      environment : "production"
    }

    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        name  = "public"
        value = "0.0.0.0/0"
      }
    }

    database_flags {
      name  = "cloudsql.iam_authentication"
      value = "on"
    }
  }

  database_version    = "POSTGRES_15"
  deletion_protection = "false"
}

resource "google_sql_database" "this" {
  name     = "python_fastapi"
  instance = google_sql_database_instance.this.id
}

resource "google_sql_user" "db_user" {
  name     = "db_user"
  instance = google_sql_database_instance.this.id
  password = var.sql_user_password
}
