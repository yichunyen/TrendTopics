resource "google_cloud_scheduler_job" "daily_trends" {
  name        = "trend-topics-daily-job"
  description = "Fetch Google Trends Taiwan daily at 9 AM"
  schedule    = "0 9 * * *"
  time_zone   = "Asia/Taipei"
  region      = var.region

  http_target {
    http_method = "POST"
    uri         = "${google_cloud_run_v2_service.trend_topics.uri}/fetch-trends"

    oidc_token {
      service_account_email = google_service_account.scheduler.email
    }
  }

  retry_config {
    retry_count = 3
  }

  depends_on = [google_project_service.required_apis]
}

resource "google_cloud_scheduler_job" "noon_trends" {
  name        = "trend-topics-noon-job"
  description = "Fetch Google Trends Taiwan daily at 12 PM"
  schedule    = "0 12 * * *"
  time_zone   = "Asia/Taipei"
  region      = var.region

  http_target {
    http_method = "POST"
    uri         = "${google_cloud_run_v2_service.trend_topics.uri}/fetch-trends"

    oidc_token {
      service_account_email = google_service_account.scheduler.email
    }
  }

  retry_config {
    retry_count = 1
  }

  depends_on = [google_project_service.required_apis]
}