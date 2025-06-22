import pandas as pd


def constructData():
    actors = pd.read_excel("testData/testActors.xlsx")
    movies = pd.read_excel("testData/testMovies.xlsx")
    ratings = pd.read_excel("testData/testRatings.xlsx")

    merge1 = pd.merge(movies, actors, on="movie", how="left")

    merge2 = pd.merge(merge1, ratings, on="movie", how="left")

    merge2['movie'] = merge2['movie'].astype(str)

    return merge2


def findMoviesByActor(data, actor):
    print(f"selected actor {actor}")
    viewingData = data[['actors', 'movie', 'title']].groupby("actors")
    return viewingData.get_group(actor).reset_index(drop=True)

def findActorsByMovie(data, movie):

    viewingData = data[['title', 'movie', 'actors']].groupby("title")

    df = data.sort_values(by=["title", "movie"]).reset_index(drop=True)


    viewingData = viewingData.get_group(movie).set_index(['title', 'movie', 'actors'])
    
    df = df[df['title'] == movie]
        # Blank out duplicate 'title' and 'movie' except for first occurrence
    df.loc[1:, 'title'] = df['title'].mask(df['title'] == df['title'].shift()).fillna('')
    df.loc[1:, 'movie'] = df['movie'].mask(df['movie'] == df['movie'].shift()).fillna('')

    return df.reset_index(drop=True)

def getActorStats(data, actor):
    averageRating = 0
    maxRating = 0
    minRating = 0

    df = data[data['actors'] == actor]

    maxRating = float(df['rating'].max())
    minRating = float(df['rating'].min())
    averageRating = float(df['rating'].mean() )

    statString = f"The maximum rating for the actor is: {maxRating}\nThe minimum rating is: {minRating}\nThe average rating is {averageRating}"

    return statString



def getMoviesForGenre(data, genre):
    mask = data['genre'].str.lower() == genre.lower()
    return data.loc[mask]

def getMoviesForReleaseData(data, year1, year2):
    mask = data['release'] > year1 & data['release'] < year2
    return data.loc[mask]

def getMoviesForRatings(data, rating):
    mask = data['rating'] > rating
    return data.loc[mask]

def getMoviesForActorActress(data, actorActress):
    #making all in the string lower for continuity -> will be much easier this way to match -> will do same in string
    actorActressCaseInsensitive = actorActress.lower()
    actorsString = data['actors'].apply( lambda actor : ','.join(actor) if isinstance(actor, list) else (actor if isinstance(actor, str) else '') )

    mask = actorsString.str.lower().str.contains(actorActressCaseInsensitive)
    return data.loc[mask]


    



