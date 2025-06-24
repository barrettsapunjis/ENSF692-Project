"""
ENSF 692 Spring 2025 - Final Project
Movie Database Analysis System - Main Application
Authors: Marley Cheema, Barrett Sapunjis
Group: 6
Description: Interactive CLI for movie database queries
"""

# The dataHandler is capable of dynamically importing the data from a pickle file if one exists under the name "realData.pkl". 
# It is suggested to add this file to the same folder as the app.py file. As its exactly what the first construction of the data is.

# If you would like to run the data construction, it may take some time and you must not include the .pkl file into the same folder as the app.py file.

# The principals file is very large and vastly increases the time of the data construction. It also does not need to be used for the program to run.
# If you would like to use the principals file, you can add it into the "customData" folder.

import pandas as pd
import dataHandler as dh
import dataStatsScript as ds


def interactiveCLI():
    """
    Main interactive command-line interface for movie database queries.
    Provides filtering options by genre, release date, actor/actress, and ratings.
    """
    data = dh.construct_data()
    og_data = data.copy()
    current_data = data

    print("\nHello! Welcome to The Movie Catalog. You wil have the ability to get a list of movies that match your specifications. \n" \
            "You can will have the option to sorts our list of over 450,000 movies by genre, release dates, actors and ratings! You can continue" \
            "filtering this list for as long as you desire \n "
            "Lets Begin: How would like to start your filtering?\n")
    


    while True:
        # 2) Filter menu
        try:
            user_in = int(input(
                "Please choose from the following options:\n"
                "[1] Filter by genre\n"
                "[2] Filter by release date\n"
                "[3] Filter by actor/actress\n"
                "[4] Filter by minimum rating\n"
                "[5] Export data to excel\n"
                "[6] Get user data analysis\n"
                "[7] Reset data\n"
                "[0] Exit\n"
                "Enter a number (0–7): "
            ))
        except ValueError:
            print("Invalid entry; please enter one of the above listed options")
            continue

        if user_in == 0:
            print("Exiting program")
            break

        # 3) Apply the selected filter
        if user_in == 1:
            genre = input("Enter a genre to filter by: ").strip()
            if genre:
                current_data = dh.get_movies_for_genre(current_data, genre)

        elif user_in == 2:
            new_in = input(f"You have selected option [{user_in}]: Get movies by release date. \n" \
                            "You now have three options.\nif you would like to filter for movies after a certain year enter : 1 \n" \
                            "If you like to filter for movie before a certain year enter : 2 \n" \
                            "If you would like to filter for movie between two years enter : 3 \n")
            release_date_option = new_in
            
            if release_date_option == "1":
                year = input("Please enter the year that you like to only see movies released after that date (not including): ").strip()
                year1 = year
                year2 = 2030
                current_data = dh.get_movies_for_release_date(current_data, year1, year2)
        
            elif release_date_option == "2":
                year = input("Please enter the year that you like to only see movies released before that date (not including):  ").strip()
                year1 = 0
                year2 = year
                current_data = dh.get_movies_for_release_date(current_data, year1, year2)

            elif release_date_option == "3":
                year1 = input("Please enter the year you would like for your lower limit (not including) ").strip()
                year2   = input("Please enter the year you would like for your upper limit (not including)").strip()
                current_data = dh.get_movies_for_release_date(current_data, year1, year2)
            
            else:
                print("Invalid option; no date filter applied.")

        elif user_in == 3:
            actor = input("Enter actor/actress name to filter by: ").strip().lower()
            if actor:
                current_data = dh.find_movies_by_actor(current_data, actor)


        elif user_in == 4:
            try:
                rating = float(input("Enter minimum rating threshold (e.g. 7.5): ").strip())
                current_data = dh.get_movies_for_ratings(current_data, rating)
            except ValueError:
                print("Invalid rating; please enter a number like 7.5.")

        elif user_in == 5:
            short_data, full_data, analysis_string = dh.get_user_data_analysis(current_data)
            dh.export_data(full_data)
        
        elif user_in == 6:
            print("\nYou have selected option [{userIn}]: Get user data analysis. \n" \
                    "You will now see a summary of the data that you have filtered by. \n")
            analysis_data, full_data, analysis_string = dh.get_user_data_analysis(current_data)
            print(analysis_data.reset_index())
            print(analysis_string)
            input("Enter any key to continue")

        elif user_in == 7:
            current_data = og_data.copy()
            print("Data has been reset")

        else:
            print("Invalid selection please enter a number between 0–7.")
            continue


        #Updating count to user to help guide decision making -> whether or not they should keep filtering
        count = len(current_data)
        print(f"\n🔍 Currently based on your selections your output list of movies has {count} entries that match the criteria!")

        if count == 0:
            print("\nNo movies left to filter—exiting. Resetting data...\n")
            current_data = og_data.copy()


        # 5) Ask whether to keep filtering this same slice
        again = input("Would you like to apply another filter on this list or select a new option? (Y/N): ").strip().lower()
        if again != 'y':
            break

    # 6) Final output
    if len(current_data) > 0:
        print("\n🎬 \033[32mHere is a sample of your final list:\033[0m")
        print(current_data.copy().reset_index().head())

        print("\n\033[32mHere is a sample of the analysed filtered data by\033[0m\n")
        analyzed_data, full_data, analysis_string = dh.get_user_data_analysis(current_data)
        print(analyzed_data.reset_index().head())
        print(analysis_string)
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        dh.export_data(full_data)

        print("\n\033[32mYour data has been exported to data.xlsx\033[0m\n")
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        input("\n\033[32mEnter any key to print the analysis for the entire dataset\033[0m\n")
        print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        ds.describe(og_data)
    
if __name__ == '__main__':
    interactiveCLI()
