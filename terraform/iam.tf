# IAM roles for trend-topics-runner to execute Terraform via Cloud Build
# This allows the service account to run terraform plan and apply

locals {
  terraform_runner_roles = [
    "roles/run.admin",                      # Manage Cloud Run services
    "roles/cloudscheduler.admin",           # Manage Cloud Scheduler jobs
    "roles/secretmanager.admin",            # Manage Secret Manager secrets
    "roles/iam.serviceAccountAdmin",        # Manage service accounts
    "roles/iam.serviceAccountUser",         # Use service accounts
    "roles/iam.securityAdmin",              # Manage IAM policies
    "roles/serviceusage.serviceUsageAdmin", # Enable/disable APIs
    "roles/artifactregistry.admin",         # Manage Artifact Registry
    "roles/storage.admin",                  # Access tfstate bucket
    "roles/logging.logWriter",              # Write Cloud Run logs
  ]
}

# Grant project-level IAM roles for Terraform operations
resource "google_project_iam_member" "terraform_runner" {
  for_each = toset(local.terraform_runner_roles)

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.cloud_run.email}"
}
