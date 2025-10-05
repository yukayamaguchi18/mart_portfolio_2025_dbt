{{ config(materialized='table') }}

select
    s.subscription_id,
    s.customer_id,
    s.product_id,
    s.contract_date,
    s.cancel_date,
    s.status,
    count(distinct o.order_id) as total_orders,
    sum(o.total_amount) as total_amount,
    max(o.order_date) as last_order_date
from {{ ref('stg_subscription') }} s
left join {{ ref('stg_order_detail') }} od on s.subscription_id = od.subscription_id
left join {{ ref('stg_order_header') }} o on od.order_id = o.order_id
group by s.subscription_id, s.customer_id, s.product_id, s.contract_date, s.cancel_date, s.status
