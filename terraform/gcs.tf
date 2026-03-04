resource "google_storage_bucket" "tw_calendar_bucket" {
  name     = "${var.project_id}-calendar-bucket"
  location = var.region
  project  = var.project_id

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  depends_on                  = [google_project_service.required_apis]
}