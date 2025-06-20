import pandas as pd
import dataHandler as dh


def interactiveCLI():
    data = dh.constructData()

    while(True):
        userIn = int(input("Please select an option for what you would like to do \n" \
                        "[1] find movies by actor \n" \
                        "[2] find actors in movie \n" \
                        "[3] find movies by date \n"))
        
        match userIn:
            case 1:
                newIn = input(f"You have selected option [{userIn}]: find movies by actor \n" \
                            "Please enter the name of the actor you would like to find or enter 0 for the main menu: ")
                if(newIn == "0"):
                    continue

                else:
                    print(userIn)
                    print(dh.findActorMovies(data, newIn))



if __name__ == '__main__':
    interactiveCLI()