variable "project_id" {
  description = "ID do projeto GCP onde os recursos serão criados"
  type        = string
}

variable "region" {
  description = "Região para o Cloud Run e localização do dataset BigQuery (ex.: us-central1)"
  type        = string
}

variable "image_url" {
  description = "URL da imagem de container para o serviço Cloud Run"
  type        = string
}

variable "dataset_id" {
  description = "ID do dataset BigQuery a ser criado"
  type        = string
}

variable "table_dados" {
  description = "Nome da tabela de dados históricos (particionada)"
  type        = string
}

variable "table_monitor" {
  description = "Nome da tabela de monitoramento de execução (particionada)"
  type        = string
}
