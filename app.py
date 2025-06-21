import pandas as pd
import dataHandler as dh


def interactiveCLI():
    data = dh.constructData()
    currentData = data

    print("Hello! Welcome to The Movie Catalog. You wil have the ability to get a list of movies that match your specifications. \n" \
            "You can will have the option to sorts our list of over 200 000 movies by genre, release dates, actors and ratings! You can continue" \
            "filtering this list for as long as you desire \n "
            "Lets Begin: How would like to start your filtering?\n")
    

    while(True):
        userIn = int(input(
                        "Please choose from the following options and enter the number of your choise"   
                        "[1] Get movies by genre. \n" \
                        "[2] Get movies by release date. \n" \
                        "[3] Get movies by actors/actresses. \n"\
                        "[4] Get movies by ratings \n"
                        " Please enter a number followed by enter \n"))
        
        match userIn:
            case 1:
                newIn = input(f"You have selected option [{userIn}]: Get movies by genre \n" \
                            "Please enter a genre that you like to filter your movie catalog by or enter 0 for the main menu: ")
                if(newIn == "0"):            
                    continue
                
                else: 
                genre = newIn
                currentData = dh.getMoviesForGenre(currentData, genre)

            case 2:
                newIn = input(f"You have selected option [{userIn}]: Get movies by release date. \n" \
                            "You now have three options, if you would like to filter for movies after a certain year enter : 1 \n
                            "If you like to filter for movie before a certain year enter : 2 \n"
                            "If you would like to filter for movie between two years enter : 3 \n")
                #optionYears = newIn

                match newIn:
                    case 1: 
                        newNewIn = input(f"You have selected option [{newIn}]: Get movies after a certain year. \n" \
                            "Please enter the year that you like to only see movies released after that date (not including)")
                        year1 = newNewIn
                        year2 = 2025
                        
                        currentData = dh.getMoviesForReleaseDate(currentData, year1, year2)

                    case 2: 
                        newNewIn = input(f"You have selected option [{newIn}]: Get movies before a certain year. \n" \
                            "Please enter the year that you like to only see movies released after that date (not including)")
                        year1 = 0
                        year2 = newNewIn
                        
                        currentData = dh.getMoviesForReleaseDate(currentData, year1, year2)

                    case 3: 
                        year1 = input(f"You have selected option [{newIn}]: Get movies between certain years. \n" \
                            "Please enter the year you would like for your lower limit (not including) ")
                        year2 = input( "Please enter the year you would like for your upper limit (not including) ")
                        currentData = dh.getMoviesForReleaseDate(currentData, year1, year2)

            case 3:
                newIn = input(f"You have selected option [{userIn}]: Get movies by Actors/Actresses. \n" \
                            "Please enter the name of actor/actress of your choice")
                actorActress = newIn
                currentData = dh.getMoviesForActorActress(currentData, actorActress)
            
            case 4:
                newIn = input(f"You have selected option [{userIn}]: Get movies by Rating. \n" \
                            "Please enter the minimum rating threshold you would like for your movie catalog: Note this according to IMDB")
                rating = newIn
                currentData = dh.getMoviesForRatings(currentData, rating)

    numberOfMoviesCurrently = len(currentData)
    again = input("Keep filtering this list? (Y/N): ").strip().lower()
        if again != 'y':
            break
    
if __name__ == '__main__':
    interactiveCLI()