import dataHandler as dh
import pandas as pd

data = dh.constructData()

print(dh.findMoviesByActor(data, "Robert Downey JR"))

print(data)