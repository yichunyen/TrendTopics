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