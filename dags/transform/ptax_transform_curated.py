from datetime import timedelta

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from plugins.operators.lakehouse_load_operator import LakehouseSQLToParquetOperator
import duckdb, pathlib

RAW_BASE = "/opt/airflow/include/raw/ptax"
CURATED_BASE = "/opt/airflow/include/curated/ptax"

def prepare_stage(ds: str, **_):
    tmp_db = pathlib.Path(f"/opt/airflow/include/tmp/duck_{ds}.duckdb")
    tmp_db.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(tmp_db))
    json_path = pathlib.Path(RAW_BASE) / ds / "cotacao.json"
    if not json_path.exists():
        raise FileNotFoundError(f"Raw PTAX not found: {json_path}")
    con.execute("CREATE SCHEMA IF NOT EXISTS stg;")
    con.execute(f\"\"\"
        CREATE OR REPLACE VIEW stg.ptax_raw AS
        SELECT * FROM read_json_auto('{json_path.as_posix()}');
    \"\"\" )
    con.close()
    return str(tmp_db)

with DAG(
    dag_id="ptax_transform_curated",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={"retry_exponential_backoff": True, "max_retry_delay": timedelta(minutes=30), "sla": timedelta(minutes=30), "on_failure_callback": __import__('dags._commons.alerts', fromlist=['slack_fail']).slack_fail, "owner": "data-eng", "retries": 1},
    tags=["transform","ptax"],
) as dag:
    stage = PythonOperator(
        task_id="stage_ptax_json",
        python_callable=prepare_stage,
        op_kwargs={"ds": "{{ ds }}"},
    )

    sql = \"\"\"
        WITH rows AS (
          SELECT
            r.value:cotacaoCompra::DOUBLE AS compra,
            r.value:cotacaoVenda::DOUBLE  AS venda,
            r.value:dataHoraCotacao::VARCHAR AS data_hora
          FROM stg.ptax_raw, UNNEST(value) AS r
        )
        SELECT
          CAST(left(data_hora,10) AS DATE) AS data,
          AVG(compra) AS media_compra,
          AVG(venda)  AS media_venda,
          COUNT(*)     AS observacoes
        FROM rows
        GROUP BY 1
        ORDER BY 1
    \"\"\"

    curated_out = LakehouseSQLToParquetOperator(
        task_id="build_curated_ptax_parquet",
        sql=sql,
        output_path=f"{CURATED_BASE}/{{{{ ds }}}}/ptax_curated.parquet",
    )

    stage >> curated_out


from airflow.operators.python import PythonOperator as _Py

def _run_quality(ds: str, **_):
    import pathlib, json
    from dags._commons.quality import ptax_basic_checks
    report_dir = pathlib.Path(f"/opt/airflow/include/quality/ptax/{ds}")
    report_dir.mkdir(parents=True, exist_ok=True)
    parquet = f"/opt/airflow/include/curated/ptax/{ds}/ptax_curated.parquet"
    result = ptax_basic_checks(parquet, ds)
    (report_dir / "report.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    if not result["passed"]:
        raise ValueError(f"Quality checks failed: {result}")

quality = _Py(
    task_id="quality_checks",
    python_callable=_run_quality,
    op_kwargs={"ds": "{{ ds }}"},
)
curated_out >> quality


from airflow.operators.python import PythonOperator as _Py2

def _run_ge(ds: str, **_):
    import pathlib, json
    from dags._commons.ge_validate import validate_ptax_parquet
    report_dir = pathlib.Path(f"/opt/airflow/include/quality/ge/ptax/{ds}")
    report_dir.mkdir(parents=True, exist_ok=True)
    parquet = f"/opt/airflow/include/curated/ptax/{ds}/ptax_curated.parquet"
    result = validate_ptax_parquet(parquet, ds)
    (report_dir / "ge_report.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    if not result["passed"]:
        raise ValueError(f"GE checks failed: {result}")

ge_validation = _Py2(
    task_id="ge_validation",
    python_callable=_run_ge,
    op_kwargs={"ds": "{{ ds }}"},
)
quality >> ge_validation
