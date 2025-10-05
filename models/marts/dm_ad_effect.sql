{{ config(materialized='table') }}

select
    a.ad_id,
    a.ad_name,
    a.ad_category,
    count(case when t.tracking_type = 'Impression' then 1 end) as impressions,
    count(case when t.tracking_type = 'Click' then 1 end) as clicks,
    count(case when t.tracking_type = 'Conversion' then 1 end) as conversions,
    count(distinct t.order_id) as total_orders,
    sum(o.total_amount) as total_amount
from {{ ref('stg_ad') }} a
left join {{ ref('stg_ad_tracking') }} t
    on a.ad_id = t.ad_id
left join {{ ref('stg_order_header') }} o
    on t.order_id = o.order_id
group by a.ad_id, a.ad_name, a.ad_category
