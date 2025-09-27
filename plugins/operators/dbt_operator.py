from airflow.models import BaseOperator
from airflow.utils.context import Context
import subprocess

class DbtRunOperator(BaseOperator):
    def __init__(self, project_dir: str, **kwargs):
        super().__init__(**kwargs)
        self.project_dir = project_dir

    def execute(self, context: Context):
        cmd = ["dbt", "run", "--project-dir", self.project_dir]
        self.log.info("Running: %s", " ".join(cmd))
        subprocess.check_call(cmd)