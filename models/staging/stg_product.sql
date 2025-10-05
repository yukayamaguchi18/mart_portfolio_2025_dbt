{{ config(materialized='view') }}

select
    product_id,
    product_name,
    product_line,
    product_category,
    price
from {{ ref('product') }}
