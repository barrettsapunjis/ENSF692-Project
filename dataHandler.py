"""
ENSF 692 Spring 2025 - Final Project
Movie Database Analysis System
Authors: Marley Cheema, Barrett Sapunjis
Description: Data handling functions for movie database analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

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
        actors["knownForTitles"] = actors["knownForTitles"].str.split(",")
        try:
            principals = pd.read_csv("customData/prinicpalsActorsActressesOnly.csv")
            #Add principals data to actor data to increase the number of movies they are connected to 
            principals = principals.dropna(subset=["nconst", "tconst"])
            principals_grouped = (
                principals.groupby("nconst")["tconst"]
                .apply(set)           # use set to remove duplicates
                .reset_index()
            )

            actors = actors.merge(principals_grouped, on="nconst", how="left")

            actors["knownForTitles"] = actors["knownForTitles"].fillna("").apply(
                lambda x: set() if x == "" else x
            )

            actors["allMovies"] = actors.apply(
                lambda row: list(set(row["knownForTitles"]) | (row["tconst"] if isinstance(row["tconst"], set) else set())), axis=1
            )
            actors = actors.drop(columns=["knownForTitles", "tconst"])
            #must explode the actors movie list into different columns
            actors = actors.explode("allMovies").reset_index()
            actors["allMovies"] = actors["allMovies"].str.strip()
        except Exception as e:
            actors.rename(columns={'knownForTitles': 'allMovies'}, inplace=True)

        #Movies pre-processing
        movies['genres'] = movies['genres'].str.split(",")
        movies = movies.drop(columns=['titleType'])
        movies = movies.drop(columns=['isAdult'])

        #ratings pre-processing
        ratings['averageRating'] = ratings['averageRating'].astype(float)
        ratings.rename(columns={'averageRating': 'rating'}, inplace=True)
        ratings['numVotes'] = ratings['numVotes'].astype(int)

        actors_only = actors[actors["primaryProfession"].str.contains("actor", case=False, na=False)]
        actresses_only = actors[actors["primaryProfession"].str.contains("actress", case=False, na=False)]

        actor_groups = actors_only.groupby("allMovies")["primaryName"].apply(list).reset_index()
        actor_groups.columns = ["tconst", "actor_list"]

        actress_groups = actresses_only.groupby("allMovies")["primaryName"].apply(list).reset_index()
        actress_groups.columns = ["tconst", "actress_list"]

        movies = movies.merge(actor_groups, on="tconst", how="left") \
                .merge(actress_groups, on="tconst", how="left")
        
        movies = movies.merge(ratings, on="tconst", how='left' )
        movies['startYear'] = movies['startYear'].fillna(0).astype(int)  # or some fill value
        movies['startYear'] = movies['startYear'].astype(int)  # or some fill value


        final_data = movies.set_index(["startYear", "primaryTitle"])
        
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
    actors_by_movie = data[data.index.get_level_values('primaryTitle').str.lower() == movie.lower()]
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


    max_rating = float(df['rating'].max())
    min_rating = float(df['rating'].min())

    average_rating = df['rating'].mean()
    

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

    highestRating = data['rating'].max()
    highestRatedMovies = data[data['rating'] == highestRating].reset_index()

    lowestRating = data['rating'].min()
    lowestRatedMovies = data[data['rating'] == lowestRating].reset_index()



    pivot = data.reset_index().pivot_table(index="startYear", values=["rating", "tconst", "numVotes"], aggfunc={"rating" : "mean", "tconst" : "count", "numVotes" : "sum"})
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
    mask = data['rating'] > rating
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

def get_user_data_analysis(datai):
    data = datai.copy()
    average_data_rating = data['rating'].mean()
    average_runtime = data['runtimeMinutes'].astype(float).mean()
    
    data['ratingDelta'] = data['rating'].astype(float) - average_data_rating
    data['runtimeDelta'] = data['runtimeMinutes'].astype(float) - average_runtime
    full_data = data
    short_data = data.drop(columns=['tconst', 'originalTitle', 'endYear', 'actor_list', 'actress_list', 'genres'])


    outputString = (f"\nThe below stats are based on the above filtered data\n"
                    f"\nTotal number of movies: {data['rating'].shape[0]}\n"
                    f"Average movie rating is: {average_data_rating:.2f}\n"
                    f"Average movie runtime is: {average_runtime:.2f} minutes\n"
                    f"Average number of votes per movie is: {data['numVotes'].mean():.2f}\n")
    
    return short_data, full_data, outputString


def averageRatingOfMoviesByYear(data):
    
    data = data.reset_index()

    averageByYear = data.groupby('startYear')['rating'].mean()

    plt.figure()
    plt.scatter(averageByYear.index.astype(int), averageByYear.values)
    plt.title("Average Movie Rating Based On Year of Release")
    plt.xlabel("Release Year")
    plt.ylabel("Average Rating")
    plt.show()
   

def averageRatingsRatingOfMoviesByYearAndGenre(data):
    
    data = data.reset_index()[["startYear","rating","genres"]]
    data = data.explode("genres").dropna(subset=["genres","rating"])

    #Realized way to many genres -> and made graph look off, so decided just to keep top 10 genres!
    top_genres = data['genres'].value_counts().nlargest(10).index
    data = data[data['genres'].isin(top_genres)]
                                     
    genreGroupsYear = data.groupby(['genres', 'startYear'])['rating'].mean().reset_index()
    
    pivotGenreGroupColumns = genreGroupsYear.pivot(index = 'startYear', columns = 'genres', values = 'rating')

    plt.figure()
    for genres in pivotGenreGroupColumns.columns:
        plt.plot(pivotGenreGroupColumns.index, pivotGenreGroupColumns[genres], marker = 'o', label=genres)
    plt.title("Average Movie Rating By Genre For Release Year")
    plt.xlabel("Year")
    plt.ylabel("Average Rating")
    plt.legend(title="Genre")
    plt.show()


def topActorsByRating(data):
    dataReset = data.reset_index() #turning all the data into columns -> as we really only need 2 columns -> rating and actors, but I want to repeat ratings for the actors in same movie so will use explode

    actorRatingData = dataReset[['rating', 'actor_list']].explode('actor_list') #this effectively takes for each actor in the list and makes a new row (ChatGPT reference here helped me find the best way to do it -> explode is awesome probably will use again in future stats functions)

    #now also want to clean up my actor list to ensure that different cases wont mess anything up
    actorRatingData['actor_list'] = actorRatingData['actor_list'].str.strip().str.title()

    topActorPivotTable = pd.pivot_table(actorRatingData, index = 'actor_list', values = 'rating', aggfunc={'rating': ['count', 'mean']})

    topActorPivotTable.columns = ['Number of Movies' , "Average Rating Across Movies"]

    topActorPivotTable = topActorPivotTable[topActorPivotTable['Number of Movies'] >= 10]

    topActorPivotTable = topActorPivotTable.sort_values('Average Rating Across Movies', ascending = False).head(10)

    return topActorPivotTable

def topActressesByRating(data):
    
    dataReset = data.reset_index() #turning all the data into columns -> as we really only need 2 columns -> rating and actors, but I want to repeat ratings for the actors in same movie so will use explode

    actressRatingData = dataReset[['rating', 'actress_list']].explode('actress_list') #this effectively takes for each actor in the list and makes a new row (ChatGPT reference here helped me find the best way to do it -> explode is awesome probably will use again in future stats functions)

    #now also want to clean up my actor list to ensure that different cases wont mess anything up
    actressRatingData['actress_list'] = actressRatingData['actress_list'].str.strip().str.title()

    topActressPivotTable = pd.pivot_table(actressRatingData, index = 'actress_list', values = 'rating', aggfunc={'rating': ['count', 'mean']})

    topActressPivotTable.columns = ['Number of Movies' , "Average Rating Across Movies"]

    topActressPivotTable = topActressPivotTable[topActressPivotTable['Number of Movies'] >= 10]

    topActressPivotTable = topActressPivotTable.sort_values('Average Rating Across Movies', ascending = False).head(10)

    return topActressPivotTable

def moviesByGenre(data):
    
    dataExploded = data.explode('genres')
    genreCount = dataExploded['genres'].value_counts()
    colours = sns.color_palette('husl', len(genreCount)) 

    bars = plt.bar(genreCount.index, genreCount.values, color = colours)   

    for i, bar in enumerate(bars):
        height = bar.get_height()    
        plt.text(bar.get_x() + bar.get_width()/2., height + 1000, f'{height:,}', ha='center', va='bottom', fontsize=8)
   
    plt.figure()
    plt.xticks(rotation=45, ha='right')
    plt.title("Number of Movies Released For Each Genre")
    plt.xlabel('Genre')
    plt.ylabel("Number of Movies Released")
    plt.tight_layout()
    plt.show()

#this function is using a linear regression (simple on that ordinary least-squares) to see if there is a connection between number of votes and rating as:

#Hypothesis
#number of votes and rating as whole. I would assume the more votes a movie gets generally its rating would be lower -> 
# as more subjected to critics from the masses where as more niche movies generally just have people who enjoy the genre/actor ect viewing them and voting which probably would be more positive in light

#Slope of the regression whether negative or positive will tell us the relationship
def votesVsRating(data):

    data = data[['numVotes', 'rating']].dropna()
    ratings = data['rating'].astype(float)
    votes = data['numVotes'].astype(int).values


    #going to log transform (shout out to ChatGPT to help me realize that this needed -> to ensure votes need the same skew, also to add plus one to avoid log of 0, so helpful for debugging!!)
    # as there is such a range of votes with movies it will make the axises look super skewed and hard to interpret -> plus for a regression need to be on same scale
    
    
    log_votes = np.log10(votes + 1)

    #fitting our data and creating the line of best fit based on the all the points!
    m, b = np.polyfit(log_votes, ratings, 1)

    #Now time to plot and include our linear regression

    plt.figure()
    plt.scatter(log_votes, ratings, alpha =0.5)

    #regression
    xRegression = np.linspace(log_votes.min(), log_votes.max(), 200)
    yRegression = m * xRegression + b

    plt.plot(xRegression, yRegression, linestyle='--')
    plt.xlabel('Number of Votes (Log Scale of 10)')
    plt.ylabel("Average rating")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    y_pred = m * log_votes + b
    ss_res = ((ratings - y_pred) ** 2).sum()
    ss_tot = ((ratings - ratings.mean())**2).sum()
    r2 = 1 - ss_res/ss_tot
    print(f"Slope (m): {m}")
    print(f"Intercept (b): {b}")
    print(f"R² = {r2:.3f}")


def export_data(data):
    data.to_excel("data.xlsx")
    return "completed"
    



