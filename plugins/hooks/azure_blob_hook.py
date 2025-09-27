from airflow.hooks.base import BaseHook

class AzureBlobHook(BaseHook):
    def get_conn(self):
        # Placeholder: implemente usando azure-storage-blob e Connection
        return None