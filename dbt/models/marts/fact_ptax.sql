-- models/marts/fact_ptax.sql
with base as (
  select * from {{ ref('stg_ptax') }}
)
select
  data,
  media_compra,
  media_venda,
  observacoes,
  -- exemplo de métrica simples
  (media_venda - media_compra) as spread
from base