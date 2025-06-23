import pandas as pd
import matplotlib.pyplot as plt
import dataHandler as dH
import numpy as np

def main():
    data = dH.construct_data()
    print(data.columns)
    print(data.head(10))

    print(len(data))
    print(f"Rows: {data.shape[0]}, Columns: {data.shape[1]}")

    print(data.shape)

    dH.averageRatingOfMoviesByYear(data)

    dH.averageRatingsRatingOfMoviesByYearAndGenre(data)

    print(dH.topActorsByRating(data))
    print(dH.topActressesByRating(data))

    dH.moviesByGenre(data)
    dH.votesVsRating(data)

if __name__ == "__main__":
    main()