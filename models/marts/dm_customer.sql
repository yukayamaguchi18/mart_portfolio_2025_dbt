{{ config(materialized='table') }}

with age_calc as (
    select customer_id,
           extract(year from age(current_date, birth_date))::int as age
    from {{ ref('stg_customer') }}
),
sub_count as (
    select customer_id, count(distinct subscription_id) as subscription_count
    from {{ ref('stg_subscription') }}
    where status = 'Active'
    group by customer_id
),
shipment_f as (
    select customer_id,
           max(shipment_id) filter (where customer_frequency = 1) as f1_shipment_id,
           max(shipment_id) filter (where customer_frequency = 2) as f2_shipment_id,
           max(order_id) filter (where customer_frequency = 1) as f1_order_id,
           max(order_id) filter (where customer_frequency = 2) as f2_order_id
    from {{ ref('dm_shipment_summary') }}
    group by customer_id
),
ad_f as (
    select s.customer_id,
           max(a.tracking_id) filter (where s.customer_frequency = 1) as f1_tracking_id,
           max(a.tracking_id) filter (where s.customer_frequency = 2) as f2_tracking_id
    from {{ ref('dm_shipment_summary') }} s
    left join {{ ref('stg_ad_tracking') }} a on s.order_id = a.order_id
    group by s.customer_id
),
rfm as (
    select customer_id,
           max(shipment_date) as last_shipment_date,
           max(customer_frequency) as f,
           sum(total_amount) as m,
           sum(case when shipment_date >= date_trunc('year', current_date) then total_amount else 0 end) as m_this_year,
           sum(case when shipment_date >= current_date - interval '12 months' then total_amount else 0 end) as m_last_12m
    from {{ ref('dm_shipment_summary') }}
    group by customer_id
)
select
    c.customer_id,
    a.age,
    (a.age/10*10)::int as age_group,
    coalesce(s.subscription_count,0) as subscription_count,
    sf.f1_shipment_id,
    sf.f2_shipment_id,
    af.f1_tracking_id,
    af.f2_tracking_id,
    (current_date - r.last_shipment_date)::int as r,
    r.f,
    r.m,
    r.m_this_year,
    r.m_last_12m
from {{ ref('stg_customer') }} c
join age_calc a on c.customer_id = a.customer_id
left join sub_count s on c.customer_id = s.customer_id
left join shipment_f sf on c.customer_id = sf.customer_id
left join ad_f af on c.customer_id = af.customer_id
left join rfm r on c.customer_id = r.customer_id
