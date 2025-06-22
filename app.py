import pandas as pd
import dataHandler as dh


def interactiveCLI():
    data = dh.constructData()
    currentData = data

    print("Hello! Welcome to The Movie Catalog. You wil have the ability to get a list of movies that match your specifications. \n" \
            "You can will have the option to sorts our list of over 200 000 movies by genre, release dates, actors and ratings! You can continue" \
            "filtering this list for as long as you desire \n "
            "Lets Begin: How would like to start your filtering?\n")
    


    while True:
        # 2) Filter menu
        try:
            userIn = int(input(
                "Please choose from the following options:\n"
                "[1] Filter by genre\n"
                "[2] Filter by release date\n"
                "[3] Filter by actor/actress\n"
                "[4] Filter by minimum rating\n"
                "Enter a number (1–4): "
            ))
        except ValueError:
            print("Invalid entry; please enter 1, 2, 3, or 4.")
            continue

        # 3) Apply the selected filter
        if userIn == 1:
            genre = input("Enter a genre to filter by: ").strip()
            if genre:
                currentData = dh.getMoviesForGenre(currentData, genre)

        elif userIn == 2:
            newIn = input(f"You have selected option [{userIn}]: Get movies by release date. \n" \
                            "You now have three options, if you would like to filter for movies after a certain year enter : 1 \n" \
                            "If you like to filter for movie before a certain year enter : 2 \n" \
                            "If you would like to filter for movie between two years enter : 3 \n")
            releaseDateOption = newIn
            
            if releaseDateOption == "1":
                year = input("Please enter the year that you like to only see movies released after that date (not including): ").strip()
                year1 = year
                year2 = 2030
                currentData = dh.getMoviesForReleaseDate(currentData, year1, year2)
        
            elif releaseDateOption == "2":
                year = input("Please enter the year that you like to only see movies released before that date (not including):  ").strip()
                year1 = 0
                year2 = year
                currentData = dh.getMoviesForReleaseDate(currentData, year1, year2)

            elif releaseDateOption == "3":
                year1 = input("Please enter the year you would like for your lower limit (not including) ").strip()
                year2   = input("Please enter the year you would like for your upper limit (not including)").strip()
                currentData = dh.getMoviesForReleaseDate(currentData, year1, year2)
            
            else:
                print("Invalid option; no date filter applied.")

        elif userIn == 3:
            actor = input("Enter actor/actress name to filter by: ").strip()
            if actor:
                currentData = dh.getMoviesForActorActress(currentData, actor)


        elif userIn == 4:
            try:
                rating = float(input("Enter minimum rating threshold (e.g. 7.5): ").strip())
                currentData = dh.getMoviesForRatings(currentData, rating)
            except ValueError:
                print("Invalid rating; please enter a number like 7.5.")

        else:
            print("Invalid selection please enter a number between1–4.")
            continue


        #Updating count to user to help guide decision making -> whether or not they should keep filtering
        count = len(currentData)
        print(f"\n🔍 Currently based on your selections your output list of movies has {count} entries that match the criteria!")

        if count == 0:
            print("No movies left to filter—exiting.")
            break

        # 5) Ask whether to keep filtering this same slice
        again = input("Would you like to apply another filter on this list? (Y/N): ").strip().lower()
        if again != 'y':
            break

    # 6) Final output
    if count > 0:
        print("\n🎬 Here’s your final list:")
        print(
            currentData
              .loc[:, ['title','release_date','genre','actors','rating']]
              .to_string(index=False)
        )
    
if __name__ == '__main__':
    interactiveCLI()