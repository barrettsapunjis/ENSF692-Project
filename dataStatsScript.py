import pandas as pd
import matplotlib.pyplot as plt
import dataHandler as dH
import numpy as np

data = dH.construct_data()

dH.averageRatingOfMoviesByYear(data)

dH.averageRatingsRatingOfMoviesByYearAndGenre(data)

print(dH.topActorsByRating(data))
print(dH.topActressesByRating(data))

dH.moviesByGenre(data)
dH.votesVsRating(data)