{{ config(materialized='view') }}

select
    customer_id,
    last_name,
    first_name,
    last_name_kana,
    first_name_kana,
    birth_date::date as birth_date,
    gender,
    member_type,
    join_date::date as join_date,
    email,
    allow_email,
    phone,
    allow_phone,
    default_delivery_id,
    allow_dm
from {{ ref('customer') }}
