# TrendTopics

Fetch Taiwan Google Trends daily trending keywords and send to Slack.

## Overview

- Uses Google Trends RSS Feed to get Taiwan's daily trending search keywords
- Automatically triggered at 9:00 AM (Asia/Taipei) daily via Cloud Scheduler
- Sends results to a specified Slack channel via Webhook

## File Structure

```
TrendTopics/
├── app/
│   ├── main.py           # Flask application
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Docker image
├── terraform/
│   ├── main.tf           # GCP resource definitions
│   ├── variables.tf      # Variable definitions
│   ├── outputs.tf        # Output values
│   └── terraform.tfvars.example
├── cloudbuild.yaml       # Cloud Build configuration
└── .gitignore
```

## Terraform Deployment

```bash
# 1. Configure variables
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your project_id and region

# 2. Initialize
terraform init

# 3. Preview changes
terraform plan -var-file=terraform.tfvars

# 4. Apply changes
terraform apply -var-file=terraform.tfvars

# 5. Deploy application
cd ..
gcloud builds submit --config=cloudbuild.yaml

# 6. Add Slack Webhook Secret manually
# GCP Console → Secret Manager → slack-webhook-url → Add new version
```

## License

MIT License
