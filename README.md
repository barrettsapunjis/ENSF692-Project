# ENSF692-Project
Data analysis group project. The purpose of the project is to combine 3 seperate (but related) data sets and create a UI for a user to query the combined dataset. 

members: Marley Cheema, Barrett Sapunjis 


The three datasets used are pulled directly from IMDB (https://datasets.imdbws.com/) and modified to a smaller form. They could not be saved as xlsx without losing data. 
- namesActorActressOnly.csv
   - originally: name.basics.tsv.gz
     - modified to only contain people whos role listed them as an actor or actress
- ratings.csv
    - originally: title.ratings.tsv.gz
    - Not modified
- titles1980.csv
    -  originaly: title.basics.tsv.gz
    -  modified to only contain information on all movies made since 1980
  
     


- how to use:
   	- `pip install -r requirements.txt`
    - `make sure to download/acquire the data sets that are not posted on git`
        - https://1drv.ms/f/c/46dad491737b36ce/EqEDtUPNf2NBsdptI45pQI0B6YA13g0AbrAMVde8SHsKIw?e=nK2J8O
   	- `python .\app.py`

    




```mermaid graph TD
classDiagram
    class App {
        + interactiveCLI() void
    }
    
    class DataHandler {
        + construct_data() DataFrame
        + add_columns(data: DataFrame) void
        + find_movies_by_actor(data: DataFrame, actor: str) DataFrame
        + find_actors_by_movie(data: DataFrame, movie: str) DataFrame
        + get_actor_stats(data: DataFrame, actor: str) str
        + get_movies_for_genre(data: DataFrame, genre: str) DataFrame
        + get_genres(data: DataFrame) array
        + get_movies_for_release_date(data: DataFrame, year1: int, year2: int) DataFrame
        + get_movies_for_ratings(data: DataFrame, rating: float) DataFrame
        + get_movies_for_actor_actress(data: DataFrame, actor_actress: str) DataFrame
        + o_print(data: any) void
        + get_user_data_analysis(data: DataFrame) tuple
        + average_rating_of_movies_by_year(data: DataFrame) void
        + average_ratings_of_movies_by_year_and_genre(data: DataFrame) void
        + top_actors_by_rating(data: DataFrame) DataFrame
        + top_actresses_by_rating(data: DataFrame) DataFrame
        + movies_by_genre(data: DataFrame) void
        + votes_vs_rating(data: DataFrame) void
        + export_data(data: DataFrame) str
    }
    
    class DataStatsScript {
        + describe(data: DataFrame) void
    }
    
    App --> DataHandler : uses
    App --> DataStatsScript : uses
```
