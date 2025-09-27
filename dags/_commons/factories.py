# dags/_commons/factories.py
from datetime import timedelta

def default_args(owner="data-eng", retries=2, retry_minutes=5):
    return {
        "owner": owner,
        "retries": retries,
        "retry_delay": timedelta(minutes=retry_minutes),
    }