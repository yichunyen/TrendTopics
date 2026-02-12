# Cloud Run Service
resource "google_cloud_run_v2_service" "trend_topics" {
  name     = "trend-topics"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {
    service_account = google_service_account.cloud_run.email

    containers {
      # Initial deployment uses Google's sample image
      # Cloud Build will update this to the actual application image
      image = "gcr.io/cloudrun/hello"

      ports {
        container_port = 8080
      }

      env {
        name  = "GCP_PROJECT_ID"
        value = var.project_id
      }
      env {
        name = "SLACK_WEBHOOK_URL"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.slack_webhook.secret_id
            version = "latest"
          }
        }
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }

    scaling {
      min_instance_count = 0
      max_instance_count = 1
    }
  }

  # Ignore image changes as Cloud Build manages the container image
  lifecycle {
    ignore_changes = [
      template[0].containers[0].image,
    ]
  }

  depends_on = [
    google_project_service.required_apis,
    google_artifact_registry_repository.trend_topics,
    google_secret_manager_secret.slack_webhook,
  ]
}
