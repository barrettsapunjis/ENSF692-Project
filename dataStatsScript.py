import pandas as pd
import matplotlib.pyplot as plt
import dataHandler as dH
import numpy as np

def describe(datai):
    """
    Computes and displays comprehensive movie database analysis including visualizations.
    Parameters: datai (DataFrame) - The movie dataset to analyze
    Returns: None
    """
    data = datai.copy().sort_index(ascending=False)
    print(f"\n\033[32mHere are the first 10 columns of the entire dataset:\033[0m\n\n{data.head(10)}")

    print(f"Rows: {data.shape[0]}, Columns: {data.shape[1]}")


    dH.average_rating_of_movies_by_year(data)

    dH.average_ratings_of_movies_by_year_and_genre(data)

    print(f"\n\033[32mPrinting the top 10 actors that have appeared in more than 10 movies\033[0m\n{dH.top_actors_by_rating(data)}")
    print(f"\n\033[32mPrinting the top 10 actresses that have appeared in more than 10 movies\033[0m\n{dH.top_actresses_by_rating(data)}")

    dH.movies_by_genre(data)
    dH.votes_vs_rating(data)

