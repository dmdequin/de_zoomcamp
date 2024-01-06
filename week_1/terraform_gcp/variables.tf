variable "credentials" {
  description = "My GCP Credentials"
  default     = "./my_creds.json"
}

variable "gcs_project_id" {
  description = "GCS Project ID"
  default     = "data-engineering-410115"
}

variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "region" {
  description = "Project Region"
  default     = "us-central1"
}

variable "bq_dataset_id" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "data-engineering-410115-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}