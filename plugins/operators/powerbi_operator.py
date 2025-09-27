# plugins/operators/powerbi_operator.py
from airflow.models import BaseOperator
from airflow.utils.context import Context
import requests, os

class PowerBIRefreshDatasetOperator(BaseOperator):
    template_fields = ("group_id","dataset_id")

    def __init__(self, group_id: str, dataset_id: str, **kwargs):
        super().__init__(**kwargs)
        self.group_id = group_id
        self.dataset_id = dataset_id

    def execute(self, context: Context):
        # Requires env var: POWERBI_TOKEN (bearer) OR implement OAuth via connection
        token = os.getenv("POWERBI_TOKEN", "").strip()
        if not token:
            self.log.warning("POWERBI_TOKEN not set; skipping refresh call.")
            return "skipped"
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.group_id}/datasets/{self.dataset_id}/refreshes"
        headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}
        resp = requests.post(url, headers=headers, json={"type":"Full"})
        if resp.status_code not in (200, 202):
            raise RuntimeError(f"Power BI refresh failed: {resp.status_code} {resp.text}")
        return f"queued:{resp.status_code}"