import dataHandler as dh
import pandas as pd

data = dh.construct_data()

print(dh.find_movies_by_actor(data, "Rupert Cole"))

print(dh.find_actors_by_movie(data, "Iron Man"))


print(dh.get_genres(data))
print(dh.get_movies_for_genre(data, "Action"))

print(dh.get_movies_for_ratings(data, 8.0))

print(dh.get_movies_for_release_date(data, 1980, 1985))

print(dh.get_actor_stats(data, "Rupert Cole"))

print(dh.describe(data))

data, full_data, dataString = dh.get_user_data_analysis(data)
print(data.reset_index())
print(dataString)