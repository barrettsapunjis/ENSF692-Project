import dataHandler as dh
import pandas as pd

data = dh.constructData()


#test finActorMovies()
actorData = dh.findMoviesByActor(data, 'rdj')

#test findMovieActors
print(f"findMoviesForActor(): \n{actorData} \n")

movieData = dh.findActorsByMovie(data, 'Iron man')
print(f"'findActorsInMovie() : \n{movieData} \n ")
print(f"{dh.getActorStats(data, 'rdj')}")

print(f"{dh.getTotalStats(data)}")

print(f"moviesForRatings(): {dh.getMoviesForRatings(data, 4)}")