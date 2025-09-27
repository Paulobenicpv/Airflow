from datetime import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from dags._commons.factories import default_args
from dags._commons.consts import TAGS_INGESTION

with DAG(
    dag_id="sap_orders_ingest",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args(),
    tags=TAGS_INGESTION,
) as dag:
    start = EmptyOperator(task_id="start")
    extract = EmptyOperator(task_id="extract_orders")
    load = EmptyOperator(task_id="load_raw_zone")
    start >> extract >> load