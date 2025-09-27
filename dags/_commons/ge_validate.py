# dags/_commons/ge_validate.py
import json, pathlib
import pandas as pd
import duckdb

def validate_ptax_parquet(parquet_path: str, ds: str) -> dict:
    # load parquet via duckdb into pandas
    con = duckdb.connect(database=":memory:")
    df = con.execute(f"SELECT * FROM read_parquet('{parquet_path}')").df()
    con.close()

    # simple "GE-like" validations (without full GE project scaffolding)
    results = {
        "row_count_gt_zero": len(df) > 0,
        "no_null_media_compra": df["media_compra"].notna().all() if "media_compra" in df else False,
        "no_null_media_venda": df["media_venda"].notna().all() if "media_venda" in df else False,
        "no_null_data": df["data"].notna().all() if "data" in df else False,
        "ds_match": df["data"].astype(str).eq(ds).all() if "data" in df else False,
        "observacoes_positive": (df["observacoes"] > 0).all() if "observacoes" in df else False,
    }
    passed = all(results.values())
    return {"passed": bool(passed), "checks": results, "rows": int(len(df))}