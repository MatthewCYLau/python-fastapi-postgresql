terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }

  backend "gcs" {
    bucket = "python-fastapi-postgresql-tf-state"
    prefix = "security/terraform/state"
  }
}

provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
}
