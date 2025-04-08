import pandas as pd

# Load the dataset
df = pd.read_csv("../data/flights_data_extended.csv")

# Brief DataFrame Explanation
print("\nDataFrame Columns Explanation:")
print("- departure_date: Flight departure date")
print("- origin/destination: Flight route")
print("- trip_type: ONE_WAY or ROUND_TRIP")
print("- requested_airline: Airline searched for ('ALL' means generic query)")
print("- actual_airlines: Actual airlines flying segments")
print("- flight_numbers: Flight numbers for segments")
print("- stops: Number of stops")
print("- duration: Itinerary duration")
print("- price/currency: Fare and its currency")

# Display first rows
print("\nFirst 5 rows:")
print(df.head())

# Summary statistics
print("\nSummary Statistics:")
print(df['price'].describe())

# Check if airline-specific searches find better prices than generic searches
print("\nChecking if airline-specific searches yielded better prices:")

# Get cheapest prices from generic searches
generic_cheapest = df[df['requested_airline'] == 'ALL'].groupby(['departure_date', 'origin', 'destination', 'trip_type']).agg({'price': 'min'}).reset_index()
generic_cheapest = generic_cheapest.rename(columns={'price': 'generic_cheapest_price'})

# Get cheapest prices from airline-specific searches
airline_specific_cheapest = df[df['requested_airline'] != 'ALL'].groupby(['departure_date', 'origin', 'destination', 'trip_type']).agg({'price': 'min'}).reset_index()
airline_specific_cheapest = airline_specific_cheapest.rename(columns={'price': 'airline_specific_cheapest_price'})

# Merge to compare
comparison_df = pd.merge(generic_cheapest, airline_specific_cheapest, on=['departure_date', 'origin', 'destination', 'trip_type'], how='inner')

# Calculate differences
comparison_df['better_price_airline_specific'] = comparison_df['airline_specific_cheapest_price'] < comparison_df['generic_cheapest_price']

# Results
better_price_cases = comparison_df[comparison_df['better_price_airline_specific']]

print(f"\nCases where airline-specific searches found better prices: {len(better_price_cases)}")
if not better_price_cases.empty:
    print(better_price_cases)
else:
    print("No better prices found in airline-specific searches compared to generic searches.")

# Count of better prices
print("\nOverall summary:")
print(comparison_df['better_price_airline_specific'].value_counts())
