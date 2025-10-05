{{ config(materialized='table') }}

select
    oh.order_id,
    oh.customer_id,
    oh.order_date,
    c.member_type as order_member_type,
    count(*) over(partition by oh.customer_id order by oh.order_date
                  rows between unbounded preceding and current row) as customer_frequency,
    oh.status,
    case when bool_or(p.product_category = 'Regular') then 'include_main' else 'trial_only' end as order_category1,
    case when bool_or(od.order_type = 'Subscription') then 'include_subscription' else 'spot_only' end as order_category2,
    string_agg(distinct od.product_id, ',') as order_product_ids,
    string_agg(distinct p.product_name, ',') as order_product_names,
    oh.total_amount,
    sum(od.quantity) as total_quantity,
    sum(case when p.product_category = 'Regular' then od.quantity else 0 end) as main_quantity,
    sum(case when p.product_category = 'Trial' then od.quantity else 0 end) as trial_quantity
from {{ ref('stg_order_header') }} oh
join {{ ref('stg_order_detail') }} od on oh.order_id = od.order_id
join {{ ref('stg_customer') }} c on oh.customer_id = c.customer_id
join {{ ref('stg_product') }} p on od.product_id = p.product_id
group by oh.order_id, oh.customer_id, oh.order_date, c.member_type, oh.status, oh.total_amount
