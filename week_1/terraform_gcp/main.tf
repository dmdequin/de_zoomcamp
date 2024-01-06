terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.10.0"
    }
  }
}

provider "google" {
  # credentials = "./data-engineering-410115-d7069ed951df.json"
  credentials = file(var.credentials)
  project     = var.gcs_project_id
  region      = var.region
}

resource "google_storage_bucket" "my_bucket_name" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id    = var.bq_dataset_id
  friendly_name = "demo"
  description   = "This is a description of the demo dataset."
  location      = var.location
}