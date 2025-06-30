# 📈 Smart Strike Microserviço

Microserviço para coleta diária de preços de fechamento e cálculo de volatilidade histórica de ações brasileiras, com persistência no BigQuery.

---

## ⚙️ Requisitos

- Conta Google Cloud com billing ativo
- Projeto criado no GCP
- Habilitar as APIs:
  - BigQuery
  - Cloud Run
  - Cloud Scheduler
  - Artifact Registry (se usar container privado)

---

## 🐍 Execução local

1. Crie um arquivo `.env` com as variáveis:

```env
BQ_PROJECT_ID=seu-projeto-id
BQ_DATASET_ID=dados_financeiros
BQ_TABELA_ID=fechamento_volatilidade
```

2. Instale dependências:

```bash
pip install -r requirements.txt
```

3. Execute o microserviço:

```bash
python main.py
```

---

## 🐳 Build Docker

```bash
docker build -t smart-strike:latest .
```

---

## ☁️ Deploy com Terraform

1. Configure suas credenciais GCP:
```bash
gcloud auth application-default login
gcloud config set project seu-projeto-id
```

2. Edite `terraform.tfvars`:
```hcl
project_id  = "seu-projeto-id"
image_url   = "gcr.io/seu-projeto-id/smart-strike:latest"
```

3. Inicialize e aplique:
```bash
cd infra
terraform init
terraform apply
```

---

## 📊 Resultados no BigQuery

A tabela `fechamento_volatilidade` conterá os dados com as colunas:
- `data`: data do fechamento
- `Ticker`: código da ação (ex: PETR4.SA)
- `Close`: preço de fechamento
- `Volatilidade`: desvio padrão dos últimos 21 dias

---

## 🧱 Arquitetura

- Clean Architecture (domain, services, repositories, pipeline)
- Python com logging e dotenv
- Infra com Terraform (Cloud Run + Scheduler + BigQuery)

---

## 📅 Agendamento

O microserviço será executado automaticamente todos os dias às 8h da manhã (BRT), via Cloud Scheduler (cron `0 11 * * *` UTC).

---

## 🧠 Autor
Philipe Augusto — Projeto prático de certificação em Machine Learning com operações em Bolsa de Valores.
