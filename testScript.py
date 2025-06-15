import pandas as pd


# Load Excel files
movies_df = pd.read_excel("testData/testNames.xlsx")      # has columns: movie_id, title
actors_df = pd.read_excel("testData/testActors.xlsx")      # has columns: movie_id, actor_name

# Group actors by movie_id into a list
actors_grouped = actors_df.groupby("movie")['actors'].apply(list).reset_index()

# Merge grouped actors into the movies dataframe
merged_df = pd.merge(movies_df, actors_grouped, on="movie", how="left")

# Rename for clarity
merged_df.rename(columns={'actor_name': 'actors'}, inplace=True)

print(merged_df)