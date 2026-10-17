resource "google_monitoring_notification_channel" "email" {
  display_name = "Database Admin Email"
  type         = "email"
  labels = {
    email_address = "lau.cy.matthew@gmail.com"
  }
}

resource "google_monitoring_alert_policy" "cloud_sql_high_cpu" {
  display_name = "Cloud SQL High CPU Utilization (> 80%)"
  combiner     = "OR"
  conditions {
    display_name = "Cloud SQL CPU utilization - 80% threshold"

    condition_threshold {
      filter          = "resource.type = \"cloudsql_database_instance\" AND metric.type = \"cloudsql.googleapis.com/database/cpu/utilization\" AND resource.label.database_id = \"${google_sql_database_instance.this.project}:${google_sql_database_instance.this.name}\""
      duration        = "300s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0.8
      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_MEAN"
      }
    }
  }

  notification_channels = [
    google_monitoring_notification_channel.email.name,
  ]

  alert_strategy {
    auto_close = "1800s"
  }
}
