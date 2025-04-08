import pandas as pd
from datetime import datetime
import os

# Load extended data
df = pd.read_csv("../data/flights_data_extended.csv")

# Feature engineering
df['departure_date'] = pd.to_datetime(df['departure_date'])
df['day_of_week'] = df['departure_date'].dt.day_name()
df['booking_lead_time'] = (df['departure_date'] - datetime.today()).dt.days

# Add route as a combined feature
df['route'] = df['origin'] + "_" + df['destination']

# Identify the cheapest offers per route/date/trip_type/source
df['rank'] = df.groupby(['departure_date', 'origin', 'destination', 'trip_type', 'source'])['price'].rank(method='first')
df['is_cheapest'] = df['rank'] == 1

# Keep only the cheapest for each group
model_df = df[df['is_cheapest']].copy()

# Select features and target
features = [
    'route', 'trip_type', 'day_of_week', 'booking_lead_time',
    'stops', 'duration', 'requested_airline', 'source'
]
target = 'actual_airlines'

model_df = model_df[features + [target]]

# Append to existing dataset if it exists
output_path = "../data/model_dataset.csv"
if os.path.exists(output_path):
    existing_df = pd.read_csv(output_path)
    model_df = pd.concat([existing_df, model_df], ignore_index=True).drop_duplicates()

# Save dataset for modeling
model_df.to_csv(output_path, index=False)
print("Model dataset updated at ../data/model_dataset.csv")
print(model_df.head())
