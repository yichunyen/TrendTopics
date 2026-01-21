
# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "run.googleapis.com",
    "cloudscheduler.googleapis.com",
    "secretmanager.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
    "cloudresourcemanager.googleapis.com",
  ])

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
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
