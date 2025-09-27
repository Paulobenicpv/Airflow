# dags/_commons/quality.py
import duckdb, pathlib

def ptax_basic_checks(parquet_path: str, ds: str) -> dict:
    """
    Run simple data quality checks on curated PTAX parquet:
      - row count > 0
      - no NULL in media_compra/media_venda/data
      - data column equals ds for this partition
      - observacoes > 0
    Returns a dict with 'passed' (bool) and 'details'.
    """
    p = pathlib.Path(parquet_path)
    con = duckdb.connect(database=":memory:")
    try:
        con.execute(f"CREATE VIEW v AS SELECT * FROM read_parquet('{p.as_posix()}');")
        cnt = con.execute("SELECT count(*) FROM v").fetchone()[0]
        nulls = con.execute("SELECT SUM((media_compra IS NULL) OR (media_venda IS NULL) OR (data IS NULL)) FROM v").fetchone()[0]
        ds_mismatch = con.execute("SELECT COUNT(*) FROM v WHERE CAST(data AS VARCHAR) <> ?", [ds]).fetchone()[0]
        obs_bad = con.execute("SELECT COUNT(*) FROM v WHERE observacoes <= 0").fetchone()[0]
        passed = (cnt > 0) and (nulls == 0) and (ds_mismatch == 0) and (obs_bad == 0)
        return {
            "passed": bool(passed),
            "details": {"rows": int(cnt), "nulls": int(nulls), "ds_mismatch": int(ds_mismatch), "obs_bad": int(obs_bad)},
        }
    finally:
        con.close()