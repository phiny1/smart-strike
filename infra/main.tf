terraform {
  required_version = ">= 1.0.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Habilita as APIs necessárias do BigQuery e Cloud Run no projeto
resource "google_project_service" "bigquery_api" {
  service           = "bigquery.googleapis.com"
  project           = var.project_id
  disable_on_destroy = false
}

resource "google_project_service" "cloud_run_api" {
  service           = "run.googleapis.com"
  project           = var.project_id
  disable_on_destroy = false
}

# Módulo para criar o dataset e tabelas BigQuery
module "bigquery" {
  source        = "./modules/bigquery"
  project_id    = var.project_id
  dataset_id    = var.dataset_id
  table_dados   = var.table_dados
  table_monitor = var.table_monitor
  region        = var.region
}

# Recurso do serviço Cloud Run definido em cloud_run.tf
