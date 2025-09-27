#!/usr/bin/env bash
set -euo pipefail
black --check .
isort --check-only .
ruff .
pytest -q
python - <<'PY'
from airflow.models import DagBag
db = DagBag(dag_folder="dags", include_examples=False)
assert len(db.import_errors) == 0, db.import_errors
PY