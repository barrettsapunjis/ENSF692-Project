import dataHandler as dh
import pandas as pd

data = dh.constructData()

print(dh.findMoviesByActor(data, "Rupert Cole"))

print(dh.findActorsByMovie(data, "Iron Man"))


print(dh.getGenres(data))
print(dh.getMoviesForGenre(data, "Action"))

print(dh.getMoviesForRatings(data, 8.0))

print(dh.getMoviesForReleaseData(data, 1980, 1985))

print(dh.getTotalStats(data))