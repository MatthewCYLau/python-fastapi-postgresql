variable "project" {
  description = "GCP project ID"
}

variable "region" {
  description = "GCP region"
}

variable "sql_user_password" {
  description = "Cloud SQL user, its password"
}

variable "resource_tags" {
  description = "Tags to set for all resources"
  type        = map(string)
  default = {
    app = "python-fastapi",
  }
}