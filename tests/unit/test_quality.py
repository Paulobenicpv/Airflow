from dags._commons.quality import ptax_basic_checks
import duckdb, pathlib, json

def test_ptax_quality_ok(tmp_path):
    # create a minimal parquet to pass checks
    p = tmp_path / "ok.parquet"
    con = duckdb.connect(database=":memory:")
    con.execute("""
        COPY (
            SELECT DATE '2025-09-01' AS data, 5.0 AS media_compra, 5.1 AS media_venda, 3 AS observacoes
        ) TO '%s' (FORMAT PARQUET)
    """ % p.as_posix())
    con.close()
    res = ptax_basic_checks(p.as_posix(), "2025-09-01")
    assert res["passed"] is True