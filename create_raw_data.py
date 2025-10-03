import pandas as pd
import random
import os
from faker import Faker
from datetime import timedelta

fake = Faker("ja_JP")

# ------------------------
# 出力フォルダ
# ------------------------
output_dir = "seed"
os.makedirs(output_dir, exist_ok=True)

# ------------------------
# マスタ件数設定
# ------------------------
num_customers = 50
num_deliveries = 80
num_products = 20
num_campaigns = 10
num_ads = 10
num_orders = 100
num_subscriptions = 20
num_tracking = 200

# ------------------------
# Customer
# ------------------------
customers = []
for i in range(1, num_customers+1):
    gender = random.choice(['Male','Female'])
    customers.append({
        'customer_id': f"C{i:04d}",
        'last_name': fake.last_name(),
        'first_name': fake.first_name_male() if gender=='Male' else fake.first_name_female(),
        'last_name_kana': fake.last_kana_name(),
        'first_name_kana': fake.first_kana_name(),
        'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=70),
        'gender': gender,
        'member_type': random.choice(['Regular','Subscription']),
        'join_date': fake.date_between(start_date='-5y', end_date='today'),
        'email': fake.email(),
        'allow_email': random.choice([0,1]),
        'phone': fake.phone_number(),
        'allow_phone': random.choice([0,1]),
        'default_delivery_id': f"D{random.randint(1,num_deliveries):04d}",
        'allow_dm': random.choice([0,1])
    })
df_customers = pd.DataFrame(customers)

# ------------------------
# Delivery
# ------------------------
deliveries = []
for i in range(1, num_deliveries+1):
    deliveries.append({
        'delivery_id': f"D{i:04d}",
        'customer_id': f"C{random.randint(1,num_customers):04d}",
        'zipcode': fake.postcode(),
        'prefecture': fake.prefecture(),
        'city': fake.city(),
        'address': fake.street_address()
    })
df_deliveries = pd.DataFrame(deliveries)

# ------------------------
# Product
# ------------------------
products = []
for i in range(1, num_products+1):
    line = random.choice(['Floral','Pure','Natural'])
    category = random.choice(['Regular','Trial'])
    products.append({
        'product_id': f"P{i:04d}",
        'product_name': f"{line} Product {i}",
        'product_line': line,
        'product_category': category,
        'price': random.randint(500,5000)
    })
df_products = pd.DataFrame(products)

# ------------------------
# Campaign
# ------------------------
campaigns = []
for i in range(1, num_campaigns+1):
    campaigns.append({
        'campaign_id': f"CP{i:03d}",
        'campaign_name': f"Campaign {i}",
        'campaign_category': random.choice(['Join','Sale','Trial'])
    })
df_campaigns = pd.DataFrame(campaigns)

# ------------------------
# Ad
# ------------------------
ads = []
for i in range(1, num_ads+1):
    ads.append({
        'ad_id': f"AD{i:03d}",
        'ad_name': f"Ad {i}",
        'ad_category': random.choice(['SNS','Listing','Offline'])
    })
df_ads = pd.DataFrame(ads)

# ------------------------
# Subscription
# ------------------------
subscriptions = []
for i in range(1, num_subscriptions+1):
    customer_id = f"C{random.randint(1,num_customers):04d}"
    product_id = f"P{random.randint(1,num_products):04d}"
    contract_date = fake.date_between(start_date='-3y', end_date='today')
    subscriptions.append({
        'subscription_id': f"S{i:04d}",
        'customer_id': customer_id,
        'status': random.choice(['Active','Cancelled']),
        'contract_date': contract_date,
        'cancel_date': fake.date_between(start_date=contract_date, end_date='today') if random.random()<0.3 else None,
        'product_id': product_id,
        'campaign_id': random.choice(df_campaigns['campaign_id'].tolist() + [None])
    })
df_subscriptions = pd.DataFrame(subscriptions)

# ------------------------
# Order Header
# ------------------------
orders = []
for i in range(1, num_orders+1):
    customer_id = f"C{random.randint(1,num_customers):04d}"
    order_date = fake.date_between(start_date='-2y', end_date='today')
    orders.append({
        'order_id': f"O{i:04d}",
        'customer_id': customer_id,
        'order_date': order_date,
        'status': random.choice(['Completed','Cancelled','Pending']),
        'total_amount': random.randint(1000,10000)
    })
df_orders = pd.DataFrame(orders)

# ------------------------
# Order Detail
# ------------------------
order_details = []
for order_id in df_orders['order_id']:
    num_items = random.randint(1,2)
    for _ in range(num_items):
        sub_flag = random.random() < 0.3
        sub_id = None
        if sub_flag and not df_subscriptions.empty:
            sub_id = random.choice(df_subscriptions['subscription_id'].tolist())
        order_details.append({
            'order_id': order_id,
            'product_id': f"P{random.randint(1,num_products):04d}",
            'order_type': 'Subscription' if sub_id else 'Spot',
            'subscription_id': sub_id,
            'quantity': random.randint(1,3),
            'campaign_id': random.choice(df_campaigns['campaign_id'].tolist() + [None])
        })
df_order_details = pd.DataFrame(order_details)

# ------------------------
# Shipment Header
# ------------------------
shipments = []
for i, row in df_orders.iterrows():
    ship_date = fake.date_between(start_date=row['order_date'], end_date='today')
    shipments.append({
        'shipment_id': f"S{i+1:04d}",
        'order_id': row['order_id'],
        'customer_id': row['customer_id'],
        'shipment_date': ship_date,
        'status': random.choice(['Shipped','Cancelled','Pending']),
        'total_amount': row['total_amount']
    })
df_shipments = pd.DataFrame(shipments)

# ------------------------
# Shipment Detail
# ------------------------
shipment_details = []
for shipment_id in df_shipments['shipment_id']:
    num_items = random.randint(1,2)
    for _ in range(num_items):
        sub_flag = random.random() < 0.3
        sub_id = None
        if sub_flag and not df_subscriptions.empty:
            sub_id = random.choice(df_subscriptions['subscription_id'].tolist())
        shipment_details.append({
            'shipment_id': shipment_id,
            'product_id': f"P{random.randint(1,num_products):04d}",
            'shipment_type': 'Subscription' if sub_id else 'Spot',
            'subscription_id': sub_id,
            'quantity': random.randint(1,3),
            'campaign_id': random.choice(df_campaigns['campaign_id'].tolist() + [None])
        })
df_shipment_details = pd.DataFrame(shipment_details)

# ------------------------
# Ad Tracking
# ------------------------
tracking = []
tracking_types = ['Click','Conversion','Impression']
for i in range(1, num_tracking+1):
    customer_id = f"C{random.randint(1,num_customers):04d}"
    ad_id = f"AD{random.randint(1,num_ads):03d}"
    track_type = random.choice(tracking_types)

    order_id = None
    track_date = None

    if track_type == 'Conversion':
        order_row = df_orders.sample(1).iloc[0]
        order_id = order_row['order_id']
        track_date = fake.date_between(start_date=order_row['order_date'], end_date='today')
    else:
        order_row = df_orders.sample(1).iloc[0]
        track_date = fake.date_between(start_date=order_row['order_date'] - timedelta(days=30), end_date=order_row['order_date'])

    tracking.append({
        'tracking_id': f"T{i:04d}",
        'customer_id': customer_id,
        'ad_id': ad_id,
        'tracking_type': track_type,
        'order_id': order_id,
        'tracking_date': track_date
    })
df_tracking = pd.DataFrame(tracking)

# ------------------------
# CSV Export
# ------------------------
df_customers.to_csv(os.path.join(output_dir,"customer.csv"), index=False)
df_deliveries.to_csv(os.path.join(output_dir,"delivery.csv"), index=False)
df_products.to_csv(os.path.join(output_dir,"product.csv"), index=False)
df_campaigns.to_csv(os.path.join(output_dir,"campaign.csv"), index=False)
df_ads.to_csv(os.path.join(output_dir,"ad.csv"), index=False)
df_subscriptions.to_csv(os.path.join(output_dir,"subscription.csv"), index=False)
df_orders.to_csv(os.path.join(output_dir,"order_header.csv"), index=False)
df_order_details.to_csv(os.path.join(output_dir,"order_detail.csv"), index=False)
df_shipments.to_csv(os.path.join(output_dir,"shipment_header.csv"), index=False)
df_shipment_details.to_csv(os.path.join(output_dir,"shipment_detail.csv"), index=False)
df_tracking.to_csv(os.path.join(output_dir,"ad_tracking.csv"), index=False)

print("All CSV files have been generated in the data/ folder!")
