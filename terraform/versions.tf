terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  # GCS backend for remote state
  # Bucket name is provided via -backend-config at init time
  # This keeps the bucket name private (not in version control)
  backend "gcs" {
    # bucket is set via: terraform init -backend-config="bucket=YOUR_BUCKET"
    prefix = "trend-topics"
  }
}
