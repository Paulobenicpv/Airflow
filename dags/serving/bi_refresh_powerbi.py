from datetime import timedelta
from datetime import datetime
from airflow import DAG
from plugins.operators.powerbi_operator import PowerBIRefreshDatasetOperator
from dags._commons.factories import default_args
from dags._commons.consts import TAGS_SERVING

with DAG(
    dag_id="bi_refresh_powerbi",
    start_date=datetime(2024, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    default_args=default_args(),
    tags=TAGS_SERVING + ["powerbi"],
) as dag:
    refresh = PowerBIRefreshDatasetOperator(
        task_id="refresh_dataset",
        group_id="{{ var.value.powerbi_group_id | default('YOUR_GROUP_ID') }}",
        dataset_id="{{ var.value.powerbi_dataset_id | default('YOUR_DATASET_ID') }}",
    )

from plugins.operators.powerbi_poll_operator import PowerBIWaitRefreshOperator

wait = PowerBIWaitRefreshOperator(
    task_id="wait_refresh",
    group_id="{{ var.value.powerbi_group_id | default('YOUR_GROUP_ID') }}",
    dataset_id="{{ var.value.powerbi_dataset_id | default('YOUR_DATASET_ID') }}",
    timeout_sec=900,
    poll_every_sec=15,
)

refresh >> wait
