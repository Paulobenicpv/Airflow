from datetime import datetime
from airflow import DAG
from plugins.operators.dbt_operator import DbtRunOperator
from dags._commons.factories import default_args
from dags._commons.consts import TAGS_TRANSFORM

with DAG(
    dag_id="sales_model_dbt",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args(),
    tags=TAGS_TRANSFORM,
) as dag:
    dbt_run = DbtRunOperator(
        task_id="dbt_run",
        project_dir="/opt/airflow/dags/../dbt",  # caminho relativo dentro do container
    )