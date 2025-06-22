import pandas as pd


# Load Excel files
movies_df = pd.read_excel("testData/testMovies.xlsx")      # has columns: movie_id, title
actors_df = pd.read_excel("testData/testActors.xlsx")      # has columns: movie_id, actor_name

# Group actors by movie_id into a list
actors_grouped = actors_df.groupby("movie")['actors'].apply(list).reset_index()

# Merge grouped actors into the movies dataframe
merged_df = pd.merge(movies_df, actors_grouped, on="movie", how="left")

# Rename for clarity
merged_df.rename(columns={'actor_name': 'actors'}, inplace=True)

#So this is code to ensure that each word within the movie name has a Capital -> along with actors.
#This is just a test but to ensure that for user input matches better -
#Also same with actors as this is important as these are names of people

merged_df['title'] = merged_df['title'].str.title()

#Function that takes the list and capitlizes
def titleize_list(lst):
    if isinstance(lst, list):
        return [name.title() for name in lst]
    else:
        return []

#applying the capitals to the values. 
merged_df['actors'] = merged_df['actors'].apply(titleize_list)

print(merged_df)