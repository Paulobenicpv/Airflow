# plugins/operators/powerbi_poll_operator.py
from airflow.models import BaseOperator
from airflow.utils.context import Context
import requests, os, time

class PowerBIWaitRefreshOperator(BaseOperator):
    template_fields = ("group_id","dataset_id","timeout_sec","poll_every_sec")

    def __init__(self, group_id: str, dataset_id: str, timeout_sec: int = 600, poll_every_sec: int = 10, **kwargs):
        super().__init__(**kwargs)
        self.group_id = group_id
        self.dataset_id = dataset_id
        self.timeout_sec = timeout_sec
        self.poll_every_sec = poll_every_sec

    def execute(self, context: Context):
        token = os.getenv("POWERBI_TOKEN", "").strip()
        if not token:
            self.log.warning("POWERBI_TOKEN not set; skipping polling.")
            return "skipped"
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.group_id}/datasets/{self.dataset_id}/refreshes?$top=1"
        headers = {"Authorization": f"Bearer {token}"}
        waited = 0
        while waited < self.timeout_sec:
            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                raise RuntimeError(f"Power BI get refreshes failed: {r.status_code} {r.text}")
            data = r.json()
            status = (data.get("value") or [{}])[0].get("status", "Unknown")
            self.log.info("Power BI refresh status: %s", status)
            if status in ("Completed", "Succeeded"):
                return "ok"
            if status in ("Failed", "Cancelled"):
                raise RuntimeError(f"Power BI refresh failed: {status}")
            time.sleep(self.poll_every_sec)
            waited += self.poll_every_sec
        raise TimeoutError("Power BI refresh did not finish within timeout")