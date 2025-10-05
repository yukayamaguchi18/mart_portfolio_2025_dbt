{{ config(materialized='view') }}

select
    shipment_id,
    order_id,
    customer_id,
    shipment_date::date as shipment_date,
    status,
    total_amount
from {{ ref('shipment_header') }}
