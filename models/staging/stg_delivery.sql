{{ config(materialized='view') }}

select
    delivery_id,
    customer_id,
    zipcode,
    prefecture,
    city,
    address
from {{ ref('delivery') }}
