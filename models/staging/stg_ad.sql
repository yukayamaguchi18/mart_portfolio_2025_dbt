{{ config(materialized='view') }}

select
    ad_id,
    ad_name,
    ad_category
from {{ ref('ad') }}
