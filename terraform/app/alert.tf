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
      filter          = "resource.type = \"cloudsql_database\" AND metric.type = \"cloudsql.googleapis.com/database/cpu/utilization\" AND resource.label.database_id = \"${google_sql_database_instance.this.project}:${google_sql_database_instance.this.name}\""
      duration        = "300s" # Evaluated over a 5-minute window
      comparison      = "COMPARISON_GT"
      threshold_value = 0.8 # 80%

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
    auto_close = "1800s" # Automatically close incident after 30 mins if CPU drops
  }
}

resource "google_monitoring_alert_policy" "cloud_sql_high_disk" {
  display_name = "Cloud SQL High Disk Utilization (> 85%)"
  combiner     = "OR"
  conditions {
    display_name = "Cloud SQL Disk utilization - 85% threshold"

    condition_threshold {
      filter          = "resource.type = \"cloudsql_database\" AND metric.type = \"cloudsql.googleapis.com/database/disk/utilization\" AND resource.label.database_id = \"${google_sql_database_instance.this.project}:${google_sql_database_instance.this.name}\""
      duration        = "300s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0.85 # 85%

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

resource "google_monitoring_alert_policy" "cloud_sql_high_connections" {
  display_name = "Cloud SQL High Connection Utilization (> 80%)"
  combiner     = "OR"
  conditions {
    display_name = "Cloud SQL Connection utilization - 80% threshold"

    condition_threshold {
      filter          = "resource.type = \"cloudsql_database\" AND metric.type = \"cloudsql.googleapis.com/database/memory/connections_utilization\" AND resource.label.database_id = \"${google_sql_database_instance.this.project}:${google_sql_database_instance.this.name}\""
      duration        = "300s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0.8 # 80% of max_connections

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

resource "google_monitoring_alert_policy" "cloud_sql_uptime" {
  display_name = "Cloud SQL Instance Down"
  combiner     = "OR"
  conditions {
    display_name = "Cloud SQL Instance uptime health check"

    condition_threshold {
      filter          = "resource.type = \"cloudsql_database\" AND metric.type = \"cloudsql.googleapis.com/database/up\" AND resource.label.database_id = \"${google_sql_database_instance.this.project}:${google_sql_database_instance.this.name}\""
      duration        = "60s"
      comparison      = "COMPARISON_LT"
      threshold_value = 1

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_NEXT_OLDER"
      }
    }
  }

  notification_channels = [
    google_monitoring_notification_channel.email.name,
  ]

  alert_strategy {
    auto_close = "1800s" # Increased to meet the 30-minute minimum API requirement
  }
}
