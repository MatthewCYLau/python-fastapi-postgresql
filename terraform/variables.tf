variable "project" {
  description = "GCP project ID"
}

variable "region" {
  description = "GCP region"
}

variable "resource_tags" {
  description = "Tags to set for all resources"
  type        = map(string)
  default = {
    app = "python-fastapi",
  }
}