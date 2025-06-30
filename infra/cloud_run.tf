resource "google_cloud_run_service" "data_collector" {
  name     = "daily-data-collector"
  location = var.region
  project  = var.project_id

  template {
    spec {
      containers {
        image = var.image_url
        # (Opcional) Defina recursos, variáveis de ambiente etc. se necessário
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  # Garante que a API Cloud Run esteja habilitada antes de criar o serviço
  depends_on = [google_project_service.cloud_run_api]
}

# Permite invocações não autenticadas (allUsers) no serviço Cloud Run
resource "google_cloud_run_service_iam_member" "noauth_invoker" {
  location = google_cloud_run_service.data_collector.location
  project  = google_cloud_run_service.data_collector.project
  service  = google_cloud_run_service.data_collector.name

  role   = "roles/run.invoker"
  member = "allUsers"
}
