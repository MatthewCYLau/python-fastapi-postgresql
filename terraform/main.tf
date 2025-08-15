terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

terraform {
  backend "gcs" {
    bucket = "python-fastapi-tf-state-001"
    prefix = "terraform/state"
  }
}

provider "google" {
  region  = var.region
  project = var.project
}

