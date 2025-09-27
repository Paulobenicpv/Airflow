from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from dags._commons.factories import default_args
from dags._commons.consts import TAGS_TRANSFORM

with DAG(
    dag_id="dbt_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args(),
    tags=TAGS_TRANSFORM + ["dbt"],
) as dag:
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dbt && dbt run --profiles-dir profiles --project-dir .",
    )
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/dbt && dbt test --profiles-dir profiles --project-dir .",
    )
    dbt_run >> dbt_test