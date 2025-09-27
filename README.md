# Airflow Project – Production Skeleton

Estrutura base para times com CI/CD e deploy em Kubernetes.

## Pastas principais
- `dags/`: DAGs por domínio (ingestion/transform/serving).
- `include/`: SQL, templates Jinja, schemas.
- `plugins/`: Operators, Hooks, Sensors, Macros reutilizáveis.
- `configs/`: variables/pools/connections (amostras – sem segredos).
- `env/`: arquivos `.env` de exemplo (NÃO commitar segredos reais).
- `ops/`: Docker, Helm (K8s) e Compose (dev local).
- `ci/`: pipelines e checks de qualidade.
- `tests/`: testes unitários e de integração (DagBag, operators, e2e).
- `dbt/` (opcional): projeto dbt acoplado/orquestrado pelo Airflow.

## Dev rápido (docker-compose)
```bash
cp env/airflow.env.sample .env
docker compose -f ops/compose/docker-compose.yml up -d
```

## Import de variáveis/pools
```bash
airflow variables import configs/variables.json
airflow pools import configs/pools.json
```

> Connections devem ser criadas via UI/CLI/Secrets Backend (ver `configs/connections.sample.json`).

## 🚀 Quick start (dev local com Docker)
```bash
# na raiz do projeto
cp env/airflow.env.sample env/airflow.env.backup  # opcional
# .env já está pronto na raiz; ajuste se quiser.

# subir serviços (inicia banco, migra e cria usuário admin/admin)
docker compose -f ops/compose/docker-compose.yml up -d airflow-init
docker compose -f ops/compose/docker-compose.yml up -d

# acessar UI do Airflow
# http://localhost:8080 (user: admin / pass: admin)
```

## ✅ GitHub Actions
O pipeline valida formatação, executa testes e checa o DagBag a cada push/PR em `main`.

## 🔧 Personalização
- Buckets: edite `RAW_BUCKET` e `CURATED_BUCKET` no `.env`.
- Executor: ajuste `AIRFLOW__CORE__EXECUTOR` no `.env` (por padrão `LocalExecutor`).
- Slack: preencha `SLACK_WEBHOOK_URL` (se usar alertas).
