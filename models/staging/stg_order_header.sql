{{ config(materialized='view') }}

select
    order_id,
    customer_id,
    order_date::date as order_date,
    status,
    total_amount
from {{ ref('order_header') }}
