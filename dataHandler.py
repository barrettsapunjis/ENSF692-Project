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

o_print_on = False


def construct_data():
    """
    Constructs and returns the main movie dataset.
    Returns: DataFrame with hierarchical index
    """
    #If ran once, pickle data will be saved and read from
    try: 
        final_data = pd.read_pickle("realData.pkl")
        print("pickle data found")
        return final_data


    except Exception as e:
        pass

    

    try:
        actors = pd.read_csv("customData/namesActorActressOnly.csv")
        movies = pd.read_csv("customData/titles1980.csv")
        ratings = pd.read_csv("customData/Ratings.csv")
    except Exception as e:
        print("Error reading actors, movies, or ratings data")
        return None
    

    #Actors pre-processing
    actors["knownForTitles"] = actors["knownForTitles"].str.split(",")
    try:
        principals = pd.read_csv("customData/principalsActorsActressesOnly.csv")
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
    except Exception as e:
        actors.rename(columns={'knownForTitles': 'allMovies'}, inplace=True)

    #must explode the actors movie list into different columns
    actors = actors.explode("allMovies").reset_index()
    actors["allMovies"] = actors["allMovies"].str.strip()

    #Movies pre-processing
    movies['genres'] = movies['genres'].str.split(",")
    movies = movies.drop(columns=['titleType'])
    movies = movies.drop(columns=['isAdult'])
    movies = movies.drop(columns=['endYear'])

    #ratings pre-processing
    ratings['averageRating'] = ratings['averageRating'].astype(float)
    ratings.rename(columns={'averageRating': 'rating'}, inplace=True)
    ratings['numVotes'] = ratings['numVotes'].astype(int)

    #filter actors and actresses
    actors_only = actors[actors["primaryProfession"].str.contains("actor", case=False, na=False)]
    actresses_only = actors[actors["primaryProfession"].str.contains("actress", case=False, na=False)]

    #group by movie and get list of actors
    actor_groups = actors_only.groupby("allMovies")["primaryName"].apply(list).reset_index()
    actor_groups.columns = ["tconst", "actor_list"]

    #group by movie and get list of actresses
    actress_groups = actresses_only.groupby("allMovies")["primaryName"].apply(list).reset_index()
    actress_groups.columns = ["tconst", "actress_list"]

    #merge actors and actresses with movies
    movies = movies.merge(actor_groups, on="tconst", how="left") \
            .merge(actress_groups, on="tconst", how="left")
    
    #convert to list if not already (could be NaN)
    movies['actor_list'] = movies['actor_list'].apply(lambda x: x if isinstance(x, list) else [])
    movies['actress_list'] = movies['actress_list'].apply(lambda x: x if isinstance(x, list) else [])

    #merge with ratings
    movies = movies.merge(ratings, on="tconst", how='left' )
    movies['startYear'] = movies['startYear'].fillna(0).astype(int)  # or some fill value
    movies['startYear'] = movies['startYear'].astype(int)  # or some fill value

    #set index
    final_data = movies.set_index(["startYear", "primaryTitle"])
    
    final_data.to_pickle("realData.pkl")

    

    o_print(final_data)

    return final_data
    

def add_columns(data):
    """
    Adds computed columns to the dataset.
    Parameters: data (DataFrame) - The dataset to add columns to
    Returns: None
    """
    data['knownCast'] = data['actor_list'] + data['actress_list']
    data['knownCast'] = data['knownCast'].apply(lambda x: len(x) if isinstance(x, list) else False)

    data['numGenres'] = data['genres'].apply(lambda x: len(x) if isinstance(x, list) else False)

def find_movies_by_actor(datai, actor):
    """
    Finds movies by actor name.
    Parameters: data (DataFrame), actor (str)
    Returns: DataFrame of movies
    """

    data = datai.copy()

    o_print(f"\nselected actor {actor}\n")
    
    #combine actor and actress lists so search both genders at once
    data['combined_list'] = data['actor_list'] + data['actress_list']
    exploded = data.explode('combined_list')

    actors_movies = exploded[exploded['combined_list'].str.lower() == actor.lower()].drop(columns=['combined_list'])
    return actors_movies


def find_actors_by_movie(datai, movie):
    """
    Finds actors for a specific movie.
    Parameters: data (DataFrame), movie (str)
    Returns: DataFrame of actors
    """
    o_print(f"\nselected movie {movie}\n")
    data = datai.copy()
    actors_by_movie = data[data.index.get_level_values('primaryTitle').str.lower() == movie.lower()]
    return actors_by_movie

def get_actor_stats(datai, actor):
    """
    Gets statistics for an actor.
    Parameters: data (DataFrame), actor (str)
    Returns: String with actor statistics
    """
    data = datai.copy()
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


def get_movies_for_genre(datai, genre):
    """
    Filters movies by genre.
    Parameters: data (DataFrame), genre (str)
    Returns: DataFrame of movies
    """
    data = datai.copy()
    o_print(f"\ngetting movies for genre {genre}\n")

    #Create a mask to filter movies by genre
    mask = data['genres'].apply(lambda x: any(genre.lower() == g.lower() for g in x) if isinstance(x, list) else False )
    return data.loc[mask]

def get_genres(datai):
    """
    Gets unique genres from dataset.
    Parameters: data (DataFrame)
    Returns: Array of unique genres
    """
    data = datai.copy()
    o_print("\ngetting genres\n")
    data = data.reset_index()
    genres = data.explode('genres')['genres'].unique()
    return genres

def get_movies_for_release_date(datai, year1, year2=None):
    """
    Filters movies by release year range.
    Parameters: data (DataFrame), year1 (int), year2 (int, optional)
    Returns: DataFrame of movies
    """
    data = datai.copy()
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

def get_movies_for_ratings(datai, rating):
    """
    Filters movies by minimum rating.
    Parameters: data (DataFrame), rating (float)
    Returns: DataFrame of movies
    """
    data = datai.copy()
    o_print(f"\ngetting movies for ratings {rating}\n")
    mask = data['rating'] > rating
    return data[mask]

def get_movies_for_actor_actress(datai, actor_actress):
    """
    Filters movies by actor/actress name.
    Parameters: data (DataFrame), actor_actress (str)
    Returns: DataFrame of movies
    """
    data = datai.copy()

    #making all in the string lower for continuity
    actor_actress_case_insensitive = actor_actress.lower()

    #Join all actors in a movie into a single string
    actors_string = data['actors'].apply( lambda actor : ','.join(actor) if isinstance(actor, list) else (actor if isinstance(actor, str) else '') )

    mask = actors_string.str.lower().str.contains(actor_actress_case_insensitive)
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

def get_user_data_analysis(datai):
    """
    Performs basic statistical analysis on the movie dataset.
    Parameters: datai (DataFrame) - The movie dataset to analyze
    Returns: Tuple of (short_data, full_data, output_string)
    """
    data = datai.copy()
    average_data_rating = data['rating'].mean()
    average_runtime = data['runtimeMinutes'].astype(float).mean()
    
    #Calculate deltas for each row based on average values
    data['ratingDelta'] = data['rating'].astype(float) - average_data_rating
    data['runtimeDelta'] = data['runtimeMinutes'].astype(float) - average_runtime
    add_columns(data)
    full_data = data
    short_data = data.drop(columns=['tconst', 'originalTitle', 'actor_list', 'actress_list', 'genres'])


    output_string =  (f"\nTotal number of movies: {data['rating'].shape[0]}\n"
                    f"Average movie rating is: {average_data_rating:.2f}\n"
                    f"Average movie runtime is: {average_runtime:.2f} minutes\n"
                    f"Average number of votes per movie is: {data['numVotes'].mean():.2f}\n")
    
    return short_data, full_data, output_string


def average_rating_of_movies_by_year(datai):
    """
    Creates a scatter plot of average movie ratings by release year.
    Parameters: datai (DataFrame) - The movie dataset
    Returns: None
    """
    data = datai.copy()
    
    data = data.reset_index()

    average_by_year = data.groupby('startYear')['rating'].mean()

    plt.figure()
    plt.scatter(average_by_year.index.astype(int), average_by_year.values)
    plt.title("Average Movie Rating Based On Year of Release")
    plt.xlabel("Release Year")
    plt.ylabel("Average Rating")
    plt.show()
   

def average_ratings_of_movies_by_year_and_genre(datai):
    """
    Creates a line plot showing average ratings by genre over time.
    Parameters: datai (DataFrame) - The movie dataset
    Returns: None
    """
    data = datai.copy()
    
    data = data.reset_index()[["startYear","rating","genres"]]
    data = data.explode("genres").dropna(subset=["genres","rating"])

    #reduce to 10 most common genres
    top_genres = data['genres'].value_counts().nlargest(10).index
    data = data[data['genres'].isin(top_genres)]


    #Group by genre and year to get average rating for each genre each year
    genre_groups_year = data.groupby(['genres', 'startYear'])['rating'].mean().reset_index()
    
    pivot_genre_group_columns = genre_groups_year.pivot(index = 'startYear', columns = 'genres', values = 'rating')


    plt.figure(figsize=(14,7))
    for genres in pivot_genre_group_columns.columns:
        plt.plot(pivot_genre_group_columns.index, pivot_genre_group_columns[genres], marker = 'o', label=genres)
    plt.title("Average Movie Rating By Genre For Release Year")
    plt.xlabel("Year")
    plt.ylabel("Average Rating")
    plt.legend(title="Genre")
    plt.show()


def top_actors_by_rating(datai):
    """
    Finds the top 10 actors by average rating who have appeared in at least 10 movies.
    Parameters: datai (DataFrame) - The movie dataset
    Returns: DataFrame with top actors and their statistics
    """
    data = datai.copy()
    data_reset = data.reset_index() 

    #Drop most columns as we only need rating and actor list
    actor_rating_data = data_reset[['rating', 'actor_list']].explode('actor_list') 
    actor_rating_data['rating'] = actor_rating_data['rating'].fillna(0)

    #Cleaning up actor list
    actor_rating_data['actor_list'] = actor_rating_data['actor_list'].str.strip().str.title()

    #Pivot table to count the number of ratings (movies) and average rating for each actor
    top_actor_pivot_table = pd.pivot_table(actor_rating_data, index = 'actor_list', values = 'rating', aggfunc={'rating': ['count', 'mean']})

    top_actor_pivot_table.columns = ['Number of Movies' , "Average Rating Across Movies"]

    top_actor_pivot_table = top_actor_pivot_table[top_actor_pivot_table['Number of Movies'] >= 10]

    top_actor_pivot_table = top_actor_pivot_table.sort_values('Average Rating Across Movies', ascending = False).head(10)

    return top_actor_pivot_table

def top_actresses_by_rating(datai):
    """
    Finds the top 10 actresses by average rating who have appeared in at least 10 movies.
    Parameters: datai (DataFrame) - The movie dataset
    Returns: DataFrame with top actresses and their statistics
    """
    data = datai.copy()
    
    data_reset = data.reset_index() 

    actress_rating_data = data_reset[['rating', 'actress_list']].explode('actress_list')

    actress_rating_data['actress_list'] = actress_rating_data['actress_list'].str.strip().str.title()

    #count the number of ratings (movies) and average rating for each actress
    top_actress_pivot_table = pd.pivot_table(actress_rating_data, index = 'actress_list', values = 'rating', aggfunc={'rating': ['count', 'mean']})

    top_actress_pivot_table.columns = ['Number of Movies' , "Average Rating Across Movies"]

    top_actress_pivot_table = top_actress_pivot_table[top_actress_pivot_table['Number of Movies'] >= 10]

    top_actress_pivot_table = top_actress_pivot_table.sort_values('Average Rating Across Movies', ascending = False).head(10)

    return top_actress_pivot_table

def movies_by_genre(datai):
    """
    Creates a bar chart showing the number of movies released for each genre.
    Parameters: datai (DataFrame) - The movie dataset
    Returns: None
    """
    data = datai.copy()
    
    data_exploded = data.explode('genres')
    genre_count = data_exploded['genres'].value_counts()
    colours = sns.color_palette('husl', len(genre_count)) 

    plt.figure(figsize=(14,7))
    bars = plt.bar(genre_count.index, genre_count.values, color = colours)   

    for i, bar in enumerate(bars):
        height = bar.get_height()    
        plt.text(bar.get_x() + bar.get_width()/2., height + 1000, f'{height:,}', ha='center', va='bottom', fontsize=8)
   
    plt.xticks(rotation=45, ha='right', fontsize=10)  # rotate and align labels
    plt.tight_layout()  # prevents label cutoff
    
    plt.title("Number of Movies Released For Each Genre")
    plt.xlabel('Genre')
    plt.ylabel("Number of Movies Released")
    plt.tight_layout()
    plt.show()


def votes_vs_rating(datai):
    """
    Performs linear regression analysis between number of votes and ratings.
    Parameters: datai (DataFrame) - The movie dataset
    Returns: None
    """
    data = datai.copy()

    #Process data for linear regression
    data = data[['numVotes', 'rating']].dropna()
    ratings = data['rating'].astype(float)
    votes = data['numVotes'].astype(int).values

    #Section will find the linear regression of the votes vs ratings data
    #ChatGPT used to provide useful functions and example uses
    #log transformartion 
    log_votes = np.log10(votes + 1)

    #fitting our data and creating the line of best fit based on the all the points!
    m, b = np.polyfit(log_votes, ratings, 1)

    #Plot a scatter of the votes vs ratings data
    plt.figure()
    plt.scatter(log_votes, ratings, alpha =0.1, s=10)

    #regression
    x_regression = np.linspace(log_votes.min(), log_votes.max(), 200)
    y_regression = m * x_regression + b

    plt.plot(x_regression, y_regression, color ='purple', linestyle='--', linewidth=2,  label='Linear Fit')
    plt.xlabel('Number of Votes (Log Scale of 10)')
    plt.ylabel("Average rating")
    plt.title("Ratings vs Number of Votes (Log Scale)", fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    #Calculate R-squared value (a representation of how well the model fits the data)
    y_pred = m * log_votes + b
    ss_res = ((ratings - y_pred) ** 2).sum()
    ss_tot = ((ratings - ratings.mean())**2).sum()
    r2 = 1 - ss_res/ss_tot

    print("\n\033[32mLinear Regression Analysis Results:\033[0m")
    print(f"Slope (m): {m}")
    print(f"Intercept (b): {b}")
    print(f"R² (accuracy metric) = {r2:.3f}")


def export_data(data):
    """
    Exports the dataset to an Excel file.
    Parameters: data (DataFrame) - The dataset to export
    Returns: String confirmation message
    """
    data.to_excel("data.xlsx")
    return "completed"
    



