{{ config(materialized='view') }}

select
    shipment_id,
    product_id,
    shipment_type,
    subscription_id,
    quantity,
    campaign_id
from {{ ref('shipment_detail') }}
