import pandas as pd

oPrintOn = True

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

        #Actors pre-processing
        #must explode the actors movie list into different columns
        actors["knownForTitles"] = actors["knownForTitles"].str.split(",")
        actors = actors.explode("knownForTitles")
        actors["knownForTitles"] = actors["knownForTitles"].str.strip()

        #Movies pre-processing
        movies['genres'] = movies['genres'].str.split(",")

        #ratings pre-processing
        ratings['averageRating'] = ratings['averageRating'].astype(float)
        ratings['numVotes'] = ratings['numVotes'].astype(int)

        actors_only = actors[actors["primaryProfession"].str.contains("actor", case=False, na=False)]
        actresses_only = actors[actors["primaryProfession"].str.contains("actress", case=False, na=False)]

        actor_groups = actors_only.groupby("knownForTitles")["primaryName"].apply(list).reset_index()
        actor_groups.columns = ["tconst", "actor_list"]

        actress_groups = actresses_only.groupby("knownForTitles")["primaryName"].apply(list).reset_index()
        actress_groups.columns = ["tconst", "actress_list"]

        movies = movies.merge(actor_groups, on="tconst", how="left") \
                .merge(actress_groups, on="tconst", how="left")
        
        movies = movies.merge(ratings, on="tconst", how='left' )
        movies['startYear'] = movies['startYear'].fillna(0).astype(int)  # or some fill value
        movies['startYear'] = movies['startYear'].astype(int)  # or some fill value


        finalData = movies.set_index(["averageRating", "startYear", "isAdult"])
        

        print(finalData)
    
        if read == False:
            finalData.to_pickle("realData.pkl")

        print(finalData)

    return finalData


def findMoviesByActor(data, actor):
    oPrint(f"\nselected actor {actor}\n")
    actorName = actor.lower()
    newData = data.copy()
    newData['combined_list'] = newData['actor_list'] + newData['actress_list']
    #data = data.drop(columns=['actor_list',"actress_list"])
    exploded = newData.explode('combined_list')

    actorsMovies = exploded[exploded['combined_list'].str.lower() == actor.lower()].drop(columns=['combined_list'])
    return actorsMovies


def findActorsByMovie(data, movie):
    oPrint(f"\nselected movie {movie}\n")
    actorsByMovie = data[data['primaryTitle'].str.lower() == movie.lower()]
    return actorsByMovie

def getActorStats(data, actor):
    oPrint(f"\nselected actor {actor}\n")
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
    oPrint("\ngetting total stats\n")
    numMovies = data['tconst'].shape[0]

    numActors = data.explode('actor_list')['actor_list'].nunique()
    numActresses = data.explode('actress_list')['actress_list'].nunique()

    highestRating = data.index.get_level_values('averageRating').max()
    highestRatedMovies = data.loc[highestRating]

    lowestRating = data.index.get_level_values('averageRating').min()
    lowestRatedMovies = data.loc[lowestRating]


    statString = (f"The total number of movies is: {numMovies}"
                  f"\nThe total number of actors is: {numActors}"
                  f"\nThe highest rated movie is: {highestRatedMovies}"
                  f"\nThe lowest rated movie is:\n{lowestRatedMovies}"
                  f"\nThe column names are: {data.columns}")

    return statString


def getMoviesForGenre(data, genre):
    oPrint(f"\ngetting movies for genre {genre}\n")
    mask = data['genres'].apply(lambda x: any(genre.lower() == g.lower() for g in x) if isinstance(x, list) else False )
    return data.loc[mask]

def getGenres(data):
    oPrint("\ngetting genres\n")
    dataClean = data.reset_index()
    genres = dataClean.explode('genres')['genres'].unique()
    return genres

def getMoviesForReleaseData(data, year1, year2=None):
    oPrint(f"\ngetting movies for release data {year1} to {year2}\n")
    if year2 is None:
        mask = data.index.get_level_values("startYear") == year1
    else:
        mask = (
            (data.index.get_level_values("startYear") > year1) & 
            (data.index.get_level_values("startYear") < year2)
            )
    
    return data[mask]

def getMoviesForRatings(data, rating):
    oPrint(f"\ngetting movies for ratings {rating}\n")
    mask = data.index.get_level_values("averageRating") > rating
    return data[mask]

def getMoviesForActorActress(data, actorActress):
    #making all in the string lower for continuity -> will be much easier this way to match -> will do same in string
    actorActressCaseInsensitive = actorActress.lower()
    actorsString = data['actors'].apply( lambda actor : ','.join(actor) if isinstance(actor, list) else (actor if isinstance(actor, str) else '') )

    mask = actorsString.str.lower().str.contains(actorActressCaseInsensitive)
    return data.loc[mask]


def oPrint(data):
    if oPrintOn == True:
        print(data)
    else:
        pass

    



