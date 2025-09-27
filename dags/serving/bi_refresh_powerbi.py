from datetime import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from dags._commons.factories import default_args
from dags._commons.consts import TAGS_SERVING

with DAG(
    dag_id="bi_refresh_powerbi",
    start_date=datetime(2024, 1, 1),
    schedule="0 6 * * *",  # 06:00 todos os dias
    catchup=False,
    default_args=default_args(),
    tags=TAGS_SERVING,
) as dag:
    trigger_refresh = EmptyOperator(task_id="trigger_refresh_dataset")