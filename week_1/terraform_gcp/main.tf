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
  project = "data-engineering-410115"
  region  = "us-central1"
}

resource "google_storage_bucket" "my_bucket_name" {
  name          = "data-engineering-410115-terra-bucket"
  location      = "US"
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