resource "google_storage_bucket" "this" {
  name          = "python-fastapi-assets"
  location      = "EUROPE-WEST2"
  storage_class = "STANDARD"
  force_destroy = true
  labels = {
    app = "python-fastapi"
  }
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}


data "google_iam_policy" "this" {
  binding {
    role = "roles/storage.objectViewer"
    members = [
      "allUsers",
    ]
  }

  binding {
    role = "roles/storage.legacyBucketReader"
    members = [
      "serviceAccount:${google_service_account.cloud_sql_instance_user.email}"
    ]
  }

  binding {
    role = "roles/storage.legacyBucketWriter"
    members = [
      "serviceAccount:${google_service_account.cloud_sql_instance_user.email}"
    ]
  }
}

resource "google_storage_bucket_iam_policy" "this" {
  bucket      = google_storage_bucket.this.name
  policy_data = data.google_iam_policy.this.policy_data
}

resource "google_storage_bucket" "assets_uniform_access" {
  name          = "python-fastapi-assets-uniform-access"
  location      = "EUROPE-WEST2"
  storage_class = "STANDARD"
  force_destroy = true
  labels = {
    app = "python-fastapi"
  }
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }

  uniform_bucket_level_access = true
  public_access_prevention    = "inherited"
}

resource "google_storage_bucket_iam_member" "iam_user_bucket_access" {
  bucket = google_storage_bucket.assets_uniform_access.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.cloud_sql_instance_user.email}"
}

resource "google_storage_bucket_iam_member" "all_users_objects_viewer" {
  bucket = google_storage_bucket.assets_uniform_access.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}