import dataHandler as dh

import pandas as pd

data = dh.construct_data()



#test finActorMovies()
actorData = dh.find_movies_by_actor(data, 'rdj')

#test findMovieActors
print(f"findMoviesForActor(): \n{actorData} \n")

movieData = dh.find_actors_by_movie(data, 'Iron man')
print(f"'findActorsInMovie() : \n{movieData} \n ")
print(f"{dh.get_actor_stats(data, 'rdj')}")

print(f"{dh.getTotalStats(data)}")

print(f"moviesForRatings(): {dh.get_movies_for_ratings(data, 4)}")

