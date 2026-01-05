resource "google_service_account" "bastion_account" {
  account_id   = "bastion-account"
  display_name = "Bastion service account"
}

resource "google_compute_instance" "bastion" {
  name         = "bastion"
  machine_type = "e2-micro"
  zone         = data.google_compute_zones.available.names[0]

  tags = ["bastion"]

  desired_status = "RUNNING"

  boot_disk {
    initialize_params {
      image = data.google_compute_image.debian.self_link
    }
  }

  network_interface {
    network    = google_compute_network.this.self_link
    subnetwork = google_compute_subnetwork.this.self_link
    access_config {
      // Ephemeral IP
    }
  }

  metadata = {
    enable-oslogin = "TRUE"
  }

  metadata_startup_script = <<SCRIPT
    sudo apt install -y postgresql-client
    psql --version
    SCRIPT

  service_account {
    email  = google_service_account.bastion_account.email
    scopes = ["cloud-platform"]
  }

}