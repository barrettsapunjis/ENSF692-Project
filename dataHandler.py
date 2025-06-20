import pandas as pd

def constructData():
    actors = pd.read_excel("testData/testActors.xlsx")
    movies = pd.read_excel("testData/testMovies.xlsx")
    ratings = pd.read_excel("testData/testRatings.xlsx")

    merge1 = pd.merge(movies, actors, on="movie", how="left")

    merge2 = pd.merge(merge1, ratings, on="movie", how="left")

    return merge2

def findActorMovies(data, actor):
    print(f"Selected actor: {actor}")
    print(data)
    # Group the data by actors and collect all their movies
    grouped = data.groupby('actors')[['title','movie']].apply(list).reset_index()
    print(grouped)
    # Filter for the specific actor
    actor_movies = grouped.loc[f"{actor}"]
    
    # Convert to DataFrame for better presentation
    result = pd.DataFrame({'movies': actor_movies})
    
    print(f"Movies featuring {actor}:")
    
    return result
