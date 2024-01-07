# Terraform and GCP Notes

## Terraform

**Execution steps:**

```terraform init```<br>
Initializes & configures the backend, installs plugins/providers, & checks out an existing configuration from a version control<br>

```terraform plan```<br>
Matches/previews local changes against a remote state, and proposes an Execution Plan.<br>

```terraform apply```<br>
Asks for approval to the proposed plan, and applies changes to cloud<br>

```terraform destroy```<br>
Removes your stack from the Cloud<br>

**After authenticating with GCP:**

```bash
# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan # -var="project=data-engineering-410115"

# Create new infra
terraform apply # -var="project=data-engineering-410115"

# Delete infra after your work, to avoid costs on any running services
terraform destroy
```

## GCP

**Project ID**: data-engineering-410115

```bash
# authenticate using GCP keys
export GOOGLE_APPLICATION_CREDENTIALS="/mnt/c/Users/dmdeq/Desktop/dezc/de_zoomcamp/week_1/terraform_gcp/my_creds.json"

# refresh token, then login:
gcloud auth application-default login

# validate config
gcloud config list
```
