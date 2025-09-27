from datetime import timedelta
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from dags._commons.factories import default_args
from dags._commons.consts import TAGS_INGESTION

def fetch_ptax(execution_date: str, **_):
    # Exemplo: salva arquivo bruto em include/tmp/{{ ds }}
    import os, pathlib
    p = pathlib.Path(f"/opt/airflow/include/tmp/{execution_date}")
    p.mkdir(parents=True, exist_ok=True)
    (p / "ptax.json").write_text('{"ok": true, "date": "%s"}' % execution_date)

from dags._commons import alerts

with DAG(
    dag_id="b3_ptax_ingest",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=True,
    default_args=default_args(),
    tags=TAGS_INGESTION,
) as dag:
    PythonOperator(
        task_id="fetch_ptax",
        python_callable=fetch_ptax,
        op_kwargs={"execution_date": "{{ ds }}"},
    )