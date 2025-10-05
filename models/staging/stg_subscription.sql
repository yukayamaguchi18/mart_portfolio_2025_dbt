{{ config(materialized='view') }}

select
    subscription_id,
    customer_id,
    status,
    contract_date::date as contract_date,
    cancel_date::date as cancel_date,
    product_id,
    campaign_id
from {{ ref('subscription') }}
