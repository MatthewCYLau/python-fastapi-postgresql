resource "google_compute_network" "this" {
  name                    = "cloud-sql-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "this" {
  name          = "cloud-sql-subnetwork"
  ip_cidr_range = cidrsubnet(local.vpc_address_space, 12, 0)
  region        = var.region
  network       = google_compute_network.this.id
}

resource "google_compute_global_address" "private_ip_address" {
  name          = "private-ip-address"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.this.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.this.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
}

resource "google_vpc_access_connector" "this" {
  name          = "vpc-access-connector"
  machine_type  = "e2-micro"
  min_instances = 2
  max_instances = 3
  subnet {
    name = google_compute_subnetwork.this.name
  }
}