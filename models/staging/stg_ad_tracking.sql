{{ config(materialized='view') }}

select
    tracking_id,
    customer_id,
    ad_id,
    tracking_type,
    order_id,
    tracking_date::date as tracking_date
from {{ ref('ad_tracking') }}
