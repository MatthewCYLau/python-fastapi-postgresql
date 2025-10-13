resource "google_service_account" "cloud_sql_instance_user" {
  account_id   = "fastapi-db-iam-user"
  display_name = "fast-api-db-iam-user"
}

resource "google_project_iam_member" "cloud_sql_instance_user" {
  project = var.project
  role    = "roles/cloudsql.instanceUser"
  member  = "serviceAccount:${google_service_account.cloud_sql_instance_user.email}"
  condition {
    title       = "resource_name_equals_cloud_sql_instance_name"
    description = "Resource name equals ${google_sql_database_instance.this.name}"
    expression  = "resource.name == 'projects/${var.project}/instances/${google_sql_database_instance.this.name}'"
  }
}

resource "google_project_iam_member" "cloud_sql_instance_user_client" {
  project = var.project
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.cloud_sql_instance_user.email}"
  condition {
    title       = "resource_name_equals_cloud_sql_instance_name"
    description = "Resource name equals ${google_sql_database_instance.this.name}"
    expression  = "resource.name == 'projects/${var.project}/instances/${google_sql_database_instance.this.name}'"
  }
}