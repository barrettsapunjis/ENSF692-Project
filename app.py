import pandas as pd
import dataHandler as dh


def interactiveCLI():
    data = dh.constructData()

    print("Hello! Welcome to The Movie Catalog. You wil have the ability to get a list of movies that match your specifications. \n" \
            "You can will have the option to sorts our list of over 200 000 movies by genre, release dates, actors and ratings! You can continue" \
            "filtering this list for as long as you desire \n "
            "Lets Begin: How would like to start your filtering?\n")
    

    while(True):
        userIn = int(input(
                        "Please choose from the following options and enter the number of your choise"   
                        "[1] Get movies by genre. \n" \
                        "[2] Get movies by release date. \n" \
                        "[3] Get movies by actors. \n"\
                        "[4] Get movies by ratings \n"
                        " Please enter a number followed by enter \n"))
        
        match userIn:
            case 1:
                newIn = input(f"You have selected option [{userIn}]: find movies by actor \n" \
                            "Please enter the name of the actor you would like to find or enter 0 for the main menu: ")
                if(newIn == "0"):            
                    continue

                else:
                    print(dh.findMoviesByActor(data, newIn))
                    print(dh.getActorStats(data, newIn))
                

            case 2:
                newIn = input(f"You have selected option [{userIn}]: find actors by movie \n" \
                            "Please enter the name of the movie you would like to see data on, or enter 0 for the main menu: ")
                if(newIn == "0"):
                    continue

                else:
                    print(userIn)
                    print(dh.findActorMovies(data, newIn))



if __name__ == '__main__':
    interactiveCLI()