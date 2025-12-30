terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  # Configure your GCS bucket for remote state
  # Uncomment and replace with your bucket name
  # backend "gcs" {
  #   bucket = "your-terraform-state-bucket"
  #   prefix = "trend-topics"
  # }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "run.googleapis.com",
    "cloudscheduler.googleapis.com",
    "secretmanager.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
  ])

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

# Artifact Registry for Docker images
resource "google_artifact_registry_repository" "trend_topics" {
  location      = var.region
  repository_id = "trend-topics"
  format        = "DOCKER"
  description   = "Docker repository for Trend Topics application"

  depends_on = [google_project_service.required_apis]
}

# Secret Manager for Slack Webhook URL
resource "google_secret_manager_secret" "slack_webhook" {
  secret_id = "slack-webhook-url"

  replication {
    auto {}
  }

  depends_on = [google_project_service.required_apis]
}

# Service Account for Cloud Run
resource "google_service_account" "cloud_run" {
  account_id   = "trend-topics-runner"
  display_name = "Trend Topics Cloud Run Service Account"
}

# Allow Cloud Run SA to access the secret
resource "google_secret_manager_secret_iam_member" "cloud_run_secret_access" {
  secret_id = google_secret_manager_secret.slack_webhook.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run.email}"
}

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

  depends_on = [
    google_project_service.required_apis,
    google_artifact_registry_repository.trend_topics,
    google_secret_manager_secret.slack_webhook,
  ]
}

# Service Account for Cloud Scheduler
resource "google_service_account" "scheduler" {
  account_id   = "trend-topics-scheduler"
  display_name = "Trend Topics Cloud Scheduler Service Account"
}

# Allow Scheduler SA to invoke Cloud Run
resource "google_cloud_run_v2_service_iam_member" "scheduler_invoker" {
  name     = google_cloud_run_v2_service.trend_topics.name
  location = google_cloud_run_v2_service.trend_topics.location
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.scheduler.email}"
}

# Cloud Scheduler Job - runs daily at 9:00 AM Taiwan time
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
