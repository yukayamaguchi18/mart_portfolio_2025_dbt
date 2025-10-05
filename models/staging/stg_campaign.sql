{{ config(materialized='view') }}

select
    campaign_id,
    campaign_name,
    campaign_category
from {{ ref('campaign') }}
