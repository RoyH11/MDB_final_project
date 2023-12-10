import pandas as pd

csv_file_path = "data/Books_rating.csv"

output_file_path = 'data/Books_rating_refactored.csv'

selected_headers = ['Title', 'User_id', 'review/score']

df = pd.read_csv(csv_file_path)

df_filtered = df.dropna(subset=['User_id', 'Title', 'review/score'])

df_first_half = df_filtered.head(len(df_filtered) // 2)

selected_columns_df = df_first_half[selected_headers].rename(columns={'review/score': 'score'})

selected_columns_df.to_csv(output_file_path, index=False)
