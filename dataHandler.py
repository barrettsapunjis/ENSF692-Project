import pandas as pd


def constructData():

    try: 
        finalData = pd.read_pickle("realData.pkl")
        print("pickle data found")
        read = True

    except Exception as e:
        read = False
        pass

    if read:
        return finalData
    
    else:

        actors = pd.read_csv("customData/namesActorActressOnly.csv")
        movies = pd.read_csv("customData/titles1980.csv")
        ratings = pd.read_csv("customData/Ratings.csv")

        #must explode the actors movie list into different columns
        actors["knownForTitles"] = actors["knownForTitles"].str.split(",")
        actors = actors.explode("knownForTitles")
        actors["knownForTitles"] = actors["knownForTitles"].str.strip()

        actors_only = actors[actors["primaryProfession"].str.contains("actor", case=False, na=False)]
        actresses_only = actors[actors["primaryProfession"].str.contains("actress", case=False, na=False)]

        actor_groups = actors_only.groupby("knownForTitles")["primaryName"].apply(list).reset_index()
        actor_groups.columns = ["tconst", "actor_list"]

        actress_groups = actresses_only.groupby("knownForTitles")["primaryName"].apply(list).reset_index()
        actress_groups.columns = ["tconst", "actress_list"]

        movies = movies.merge(actor_groups, on="tconst", how="left") \
                .merge(actress_groups, on="tconst", how="left")
        
        movies = movies.merge(ratings, on="tconst", how='left' )

        finalData = movies.set_index(["averageRating", "startYear", "isAdult"])
    
        if read == False:
            finalData.to_pickle("realData.pkl")

        print(finalData)

    return finalData


def findMoviesByActor(data, actor):
    actorName = actor.lower()
    print(f"\nselected actor {actor}\n")

    mask = (
        data["actor_list"].apply(lambda actors: any(actorName == a.lower() for a in actors) if isinstance(actors, list) else False) |
        data["actress_list"].apply(lambda actresses: any(actorName == a.lower() for a in actresses) if isinstance(actresses, list) else False)
    )
    return data[mask]


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


def getMoviesForGenre(data, genre):
    dataClean = data.reset_index()
    mask = dataClean['genre'].str.lower() == genre.lower()
    return dataClean.loc[mask]

def getMoviesForReleaseData(data, year1, year2):
    dataClean = data.reset_index()
    mask = dataClean['release'] > year1 & data['release'] < year2
    return dataClean.loc[mask]

def getMoviesForRatings(data, rating):
    dataClean = data.reset_index()
    mask = dataClean['rating'] > rating
    return dataClean.loc[mask]

def getMoviesForActorActress(data, actorActress):
    #making all in the string lower for continuity -> will be much easier this way to match -> will do same in string
    actorActressCaseInsensitive = actorActress.lower()
    actorsString = data['actors'].apply( lambda actor : ','.join(actor) if isinstance(actor, list) else (actor if isinstance(actor, str) else '') )

    mask = actorsString.str.lower().str.contains(actorActressCaseInsensitive)
    return data.loc[mask]


    



