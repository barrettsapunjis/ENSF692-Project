import pandas as pd

def constructData():
    actors = pd.read_excel("testData/testActors.xlsx")
    movies = pd.read_excel("testData/testMovies.xlsx")
    ratings = pd.read_excel("testData/testRatings.xlsx")

    merge1 = pd.merge(movies, actors, on="movie", how="left")

    merge2 = pd.merge(merge1, ratings, on="movie", how="left")

    return merge2

def findActorMovies(data, actor):
    print(f"selected actor {actor}")
    viewingData = data.groupby("actors")["movie"]
    grouped = pd.DataFrame(viewingData)
    print(grouped)
    return grouped[f"{actor}"][:]