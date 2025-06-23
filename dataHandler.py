"""
ENSF 692 Spring 2025 - Final Project
Movie Database Analysis System
Authors: Marley Cheema, Barrett Sapunjis
Description: Data handling functions for movie database analysis
"""

import pandas as pd

o_print_on = True


def construct_data():
    """
    Constructs and returns the main movie dataset.
    Returns: DataFrame with hierarchical index
    """
    try: 
        final_data = pd.read_pickle("realData.pkl")
        print("pickle data found")
        read = True

    except Exception as e:
        read = False
        pass

    if read:
        return final_data
    
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
        movies = movies.drop(columns=['titleType'])
        movies = movies.drop(columns=['isAdult'])

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


        final_data = movies.set_index(["averageRating", "startYear"])
        
        add_columns(final_data)
    
        if read == False:
            final_data.to_pickle("realData.pkl")

        

        o_print(final_data)

        return final_data
    
def add_columns(data):
    data['knownCast'] = data['actor_list'] + data['actress_list']
    data['knownCast'] = data['knownCast'].apply(lambda x: len(x) if isinstance(x, list) else False)

    data['numGenres'] = data['genres'].apply(lambda x: len(x) if isinstance(x, list) else False)

def find_movies_by_actor(data, actor):
    """
    Finds movies by actor name.
    Parameters: data (DataFrame), actor (str)
    Returns: DataFrame of movies
    """

    data = data.copy()
    o_print(f"\nselected actor {actor}\n")
    data['combined_list'] = data['actor_list'] + data['actress_list']
    exploded = data.explode('combined_list')

    actors_movies = exploded[exploded['combined_list'].str.lower() == actor.lower()].drop(columns=['combined_list'])
    return actors_movies


def find_actors_by_movie(data, movie):
    """
    Finds actors for a specific movie.
    Parameters: data (DataFrame), movie (str)
    Returns: DataFrame of actors
    """
    o_print(f"\nselected movie {movie}\n")
    actors_by_movie = data[data['primaryTitle'].str.lower() == movie.lower()]
    return actors_by_movie

def get_actor_stats(data, actor):
    """
    Gets statistics for an actor.
    Parameters: data (DataFrame), actor (str)
    Returns: String with actor statistics
    """
    o_print(f"\nselected actor {actor}\n")
    average_rating = 0
    max_rating = 0
    min_rating = 0

    df = find_movies_by_actor(data, actor)


    max_rating = float(df.index.get_level_values('averageRating').max())
    min_rating = float(df.index.get_level_values('averageRating').min())

    ratings_list = df.index.get_level_values('averageRating').tolist()
    average_rating = sum(ratings_list) / len(ratings_list)

    stat_string = (f"The maximum rating for the actor is: {max_rating}"
                  f"\nThe minimum rating is: {min_rating}"
                  f"\nThe average rating is {average_rating}")

    return stat_string

def describe(datai):
    """
    Gets descriptive statistics for the dataset.
    Parameters: data (DataFrame)
    Returns: String with dataset statistics including pivot table
    """
    o_print("\ngetting total stats\n")
    data = datai.copy()
    numMovies = data['tconst'].shape[0]

    numActors = data.explode('actor_list')['actor_list'].nunique()
    numActresses = data.explode('actress_list')['actress_list'].nunique()

    highestRating = data.index.get_level_values('averageRating').max()
    highestRatedMovies = data.loc[highestRating].reset_index()

    lowestRating = data.index.get_level_values('averageRating').min()
    lowestRatedMovies = data.loc[lowestRating].reset_index()



    pivot = data.reset_index().pivot_table(index="startYear", values=["averageRating", "tconst", "numVotes"], aggfunc={"averageRating" : "mean", "tconst" : "count", "numVotes" : "sum"})
    #renamoing pivot table column name 'tconst' to 'numMovies'
    pivot.rename(columns={'tconst': 'numMovies'}, inplace=True)

    stat_string = (f"The total number of movies is: {numMovies}"
                  f"\nThe total number of actors is: {numActors + numActresses}"
                  f"\nThe highest rated movie(s) has a rating of {highestRating}: \n{highestRatedMovies}"
                  f"\nThe lowest rated movie is:\n{lowestRatedMovies}"
                  f"\nThe column names are: {data.columns}"
                  f"\nTable containing annual stats: \n{pivot}")
    

    return stat_string 


def get_movies_for_genre(data, genre):
    """
    Filters movies by genre.
    Parameters: data (DataFrame), genre (str)
    Returns: DataFrame of movies
    """
    o_print(f"\ngetting movies for genre {genre}\n")
    mask = data['genres'].apply(lambda x: any(genre.lower() == g.lower() for g in x) if isinstance(x, list) else False )
    return data.loc[mask]

def get_genres(data):
    """
    Gets unique genres from dataset.
    Parameters: data (DataFrame)
    Returns: Array of unique genres
    """
    o_print("\ngetting genres\n")
    data = data.reset_index()
    genres = data.explode('genres')['genres'].unique()
    return genres

def get_movies_for_release_date(data, year1, year2=None):
    """
    Filters movies by release year range.
    Parameters: data (DataFrame), year1 (int), year2 (int, optional)
    Returns: DataFrame of movies
    """
    year1 = int(year1)

    o_print(f"\ngetting movies for release data {year1} to {year2}\n")
    if year2 is None:
        mask = data.index.get_level_values("startYear") == year1
    else:
        year2 = int(year2) 
        mask = (
            (data.index.get_level_values("startYear") > year1) & 
            (data.index.get_level_values("startYear") < year2)
            )
    
    return data[mask]

def get_movies_for_ratings(data, rating):
    """
    Filters movies by minimum rating.
    Parameters: data (DataFrame), rating (float)
    Returns: DataFrame of movies
    """
    o_print(f"\ngetting movies for ratings {rating}\n")
    mask = data.index.get_level_values("averageRating") > rating
    return data[mask]

def get_movies_for_actor_actress(data, actorActress):
    """
    Filters movies by actor/actress name.
    Parameters: data (DataFrame), actorActress (str)
    Returns: DataFrame of movies
    """
    #making all in the string lower for continuity -> will be much easier this way to match -> will do same in string
    actorActressCaseInsensitive = actorActress.lower()
    actorsString = data['actors'].apply( lambda actor : ','.join(actor) if isinstance(actor, list) else (actor if isinstance(actor, str) else '') )

    mask = actorsString.str.lower().str.contains(actorActressCaseInsensitive)
    return data.loc[mask]


def o_print(data):
    """
    Optional print function controlled by oPrintOn flag.
    Parameters: data (any)
    Returns: None
    """
    if o_print_on == True:
        print(data)
    else:
        pass

def printPivot(data):

    #pivot = data.pivot_table(index="primaryTitle", columns)
    pass

def export_data(data):
    data.to_excel("data.xlsx")
    



