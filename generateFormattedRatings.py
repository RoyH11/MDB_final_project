import pandas as pd

# Path to your CSV file
csv_file_path = "data/Books_rating.csv"

output_file_path = 'data/Books_rating_refactored.csv'

# Specify the headers you want to keep
selected_headers = ['Title', 'User_id', 'review/score']

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Filter out rows where 'User_id' is missing
df_filtered = df.dropna(subset=['User_id', 'Title'])

# Create a new DataFrame with only the selected columns
selected_columns_df = df_filtered[selected_headers]

selected_columns_df = selected_columns_df.rename(columns={'review/score': 'score'})

# Save the new DataFrame to a new CSV file
selected_columns_df.to_csv(output_file_path, index=False)