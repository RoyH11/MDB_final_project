import pandas as pd

# Path to your CSV file
csv_file_path = "data/Books_rating.csv"

# Number of records to randomly sample
sample_size = 300000

# Read the entire CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Shuffle the DataFrame to ensure randomness
df_shuffled = df.sample(frac=1, random_state=42)

# Take the first 300k records from the shuffled DataFrame
random_sample = df_shuffled.head(sample_size)

# Save the random sample to a new CSV file
random_sample.to_csv("data/Books_rating_small.csv", index=False)