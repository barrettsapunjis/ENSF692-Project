import dataHandler as dh

data = dh.constructData()

#test finActorMovies()
actorData = dh.findMoviesByActor(data, 'rdj')

#test findMovieActors
print(f"findMoviesForActor(): \n{actorData} \n")

movieData = dh.findActorsByMovie(data, 'Iron man')
print(f"'findActorsInMovie() : \n{movieData} \n ")
