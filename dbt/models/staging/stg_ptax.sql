-- models/staging/stg_ptax.sql
-- Reads all curated PTAX parquet partitions and exposes basic columns
with src as (
  select * from read_parquet('/opt/airflow/include/curated/ptax/*/ptax_curated.parquet')
)
select
  cast(data as date) as data,
  cast(media_compra as double) as media_compra,
  cast(media_venda  as double) as media_venda,
  cast(observacoes as int)     as observacoes
from src