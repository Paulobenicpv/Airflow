from airflow.hooks.base import BaseHook
import duckdb

class DuckDBHook(BaseHook):
    conn_name_attr = "duckdb_conn_id"
    default_conn_name = "duckdb_default"

    def __init__(self, duckdb_conn_id: str = default_conn_name) -> None:
        super().__init__()
        self.duckdb_conn_id = duckdb_conn_id

    def get_conn(self):
        # Para produção, ler de Connection/Extra/Env
        return duckdb.connect(database=":memory:")