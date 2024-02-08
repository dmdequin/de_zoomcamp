# Week 2: Mage Notes

Build docker image
```docker compose build```

Update mage image:
```docker pull mageai/mageai:latest```


```docker compose up```

Clean up docker objects
```docker image/volume/container prune```

## Extra stuff
Check process listening to a port
 ```sudo ss -lptn 'sport = :5432'```

Kill the process
```sudo kill <process ID>```

```python
# standardize columns
data.columns = (
        data.columns
        .str.replace(' ', '_')
        .str.lower()
    )
```

```bash
# authenticate using GCP keys
export GOOGLE_APPLICATION_CREDENTIALS="/mnt/c/Users/dmdeq/Desktop/dezc/de_zoomcamp/week_1/terraform_gcp/my_creds.json"

# refresh token, then login:
gcloud auth application-default login
```

```bash
# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan # -var="project=data-engineering-410115"

# sqlpassword: postgres

# Create new infra
terraform apply # -var="project=data-engineering-410115"

# Delete infra after your work, to avoid costs on any running services
terraform destroy
```

Steps not explained in the course:
1. Delete load_balancer.tf file
2. Comment out 165-168 in main.tf
3. In variables.tj change:
    - project ID to my project ID
    - region and zone to european
4. Enabling Cloud Filestore API
5. Additional permittions in IAM