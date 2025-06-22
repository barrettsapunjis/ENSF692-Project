import pandas as pd


def constructData():
    actors = pd.read_excel("testData/testActors.xlsx")
    movies = pd.read_excel("testData/testMovies.xlsx")
    ratings = pd.read_excel("testData/testRatings.xlsx")

    merge1 = pd.merge(movies, actors, on="movie", how="left")

    merge2 = pd.merge(merge1, ratings, on="movie", how="left")

    merge2['movie'] = merge2['movie'].astype(str)

    final = merge2.set_index(['title', 'actors'])

    return final


def findMoviesByActor(data, actor):
    print(f"\nselected actor {actor}\n")
    moviesByActor = data.reset_index()
    viewingData = moviesByActor.groupby("actors")
    return viewingData.get_group(actor).reset_index(drop=True)

def findActorsByMovie(data, movie):
    print(f"\nselected movie {movie}\n")
    actorsByMovie = data.loc[movie, :]
    return actorsByMovie

def getActorStats(data, actor):
    print(f"\nselected actor {actor}\n")
    averageRating = 0
    maxRating = 0
    minRating = 0

    df = data.loc[:, actor, :]


    maxRating = float(df['rating'].max())
    minRating = float(df['rating'].min())
    averageRating = float(df['rating'].mean() )

    statString = (f"The maximum rating for the actor is: {maxRating}"
                  f"\nThe minimum rating is: {minRating}"
                  f"\nThe average rating is {averageRating}")

    return statString

def getTotalStats(data):
    print("\ngetting total stats\n")
    numMovies = data.index.get_level_values('title').nunique()
    numActors = data.index.get_level_values('actors').nunique()

    highestRatedMovie = data['rating'].max()
    lowestRatedMovie = data['rating'].min()

    actorWithMostMovies = data.index.get_level_values('actors').value_counts().idxmax()

    statString = (f"The total number of movies is: {numMovies}"
                  f"\nThe total number of actors is: {numActors}"
                  f"\nThe highest rated movie is: {highestRatedMovie}"
                  f"\nThe lowest rated movie is: {lowestRatedMovie}"
                  f"\nThe actor with the most movies is: {actorWithMostMovies}\n")

    return statString

