resource "google_artifact_registry_repository" "trend_topics" {
  location      = var.region
  repository_id = "trend-topics"
  format        = "DOCKER"
  description   = "Docker repository for Trend Topics application"

  depends_on = [google_project_service.required_apis]
}