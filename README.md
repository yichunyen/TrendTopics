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

Copyright (c) 2025 Yi-Chun Yen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
