# dags/_commons/alerts.py
import os, json, requests

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "").strip()

def _post_to_slack(payload: dict):
    if not SLACK_WEBHOOK_URL:
        return  # silently skip if not configured
    try:
        requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"}, timeout=10)
    except Exception:
        # avoid breaking the task due to alert errors
        pass

def slack_fail(context):
    dag_id = context.get("dag").dag_id if context.get("dag") else "unknown_dag"
    task_id = context.get("task_instance").task_id if context.get("task_instance") else "unknown_task"
    run_id = context.get("run_id", "manual")
    ti = context.get("task_instance")
    log_url = getattr(ti, "log_url", "")
    msg = f":rotating_light: *Airflow Failure* | DAG `{dag_id}` task `{task_id}` run `{run_id}`"
    payload = {"text": msg + (f"\nLogs: {log_url}" if log_url else "")}
    _post_to_slack(payload)