variable "project_id" {
  type = string
}

variable "dataset_id" {
  type = string
}

variable "table_dados" {
  type = string
}

variable "table_monitor" {
  type = string
}

variable "region" {
  type = string
}

# Cria o dataset BigQuery
resource "google_bigquery_dataset" "dataset" {
  dataset_id  = var.dataset_id
  project     = var.project_id
  location    = var.region

  description = "Dataset para armazenar dados históricos e monitoramento de execução"
}

# Cria a tabela particionada para dados históricos
resource "google_bigquery_table" "historical" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  project    = var.project_id
  table_id   = var.table_dados

  time_partitioning {
    type = "DAY"
  }

  schema = <<EOF
[
  {
    "name": "timestamp",
    "type": "TIMESTAMP",
    "mode": "REQUIRED"
  },
  {
    "name": "valor",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF

  # Garante que o dataset já exista antes de criar a tabela
  depends_on = [google_bigquery_dataset.dataset]
}

# Cria a tabela particionada para monitoramento de execução
resource "google_bigquery_table" "monitoring" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  project    = var.project_id
  table_id   = var.table_monitor

  time_partitioning {
    type = "DAY"
  }

  schema = <<EOF
[
  {
    "name": "execution_time",
    "type": "TIMESTAMP",
    "mode": "REQUIRED"
  },
  {
    "name": "status",
    "type": "STRING",
    "mode": "NULLABLE"
  }
]
EOF

  depends_on = [google_bigquery_dataset.dataset]
}
