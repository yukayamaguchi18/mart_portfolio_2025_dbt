{{ config(materialized='view') }}

select
    order_id,
    product_id,
    order_type,
    subscription_id,
    quantity,
    campaign_id
from {{ ref('order_detail') }}
