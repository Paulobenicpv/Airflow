import pytest
from airflow.models import DagBag

def test_dag_import():
    dag_bag = DagBag(dag_folder="dags", include_examples=False)
    assert len(dag_bag.import_errors) == 0, f"Import errors: {dag_bag.import_errors}"