"""
ENSF 692 Spring 2025 - Final Project
Movie Database Analysis System - Main Application
Authors: Marley Cheema, Barrett Sapunjis
Description: Interactive CLI for movie database queries
"""

import pandas as pd
import dataHandler as dh


def interactiveCLI():
    """
    Main interactive command-line interface for movie database queries.
    Provides filtering options by genre, release date, actor/actress, and ratings.
    """
    data = dh.construct_data()
    og_data = data.copy()
    current_data = data

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
                "[5] Export data to excel\n"
                "[6] Get user data analysis\n"
                "Enter a number (1–6): "
            ))
        except ValueError:
            print("Invalid entry; please enter 1, 2, 3, or 4.")
            continue

        # 3) Apply the selected filter
        if userIn == 1:
            genre = input("Enter a genre to filter by: ").strip()
            if genre:
                current_data = dh.get_movies_for_genre(current_data, genre)

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
                current_data = dh.get_movies_for_release_date(current_data, year1, year2)
        
            elif releaseDateOption == "2":
                year = input("Please enter the year that you like to only see movies released before that date (not including):  ").strip()
                year1 = 0
                year2 = year
                current_data = dh.get_movies_for_release_date(current_data, year1, year2)

            elif releaseDateOption == "3":
                year1 = input("Please enter the year you would like for your lower limit (not including) ").strip()
                year2   = input("Please enter the year you would like for your upper limit (not including)").strip()
                current_data = dh.get_movies_for_release_date(current_data, year1, year2)
            
            else:
                print("Invalid option; no date filter applied.")

        elif userIn == 3:
            actor = input("Enter actor/actress name to filter by: ").strip().lower()
            if actor:
                current_data = dh.find_movies_by_actor(current_data, actor)


        elif userIn == 4:
            try:
                rating = float(input("Enter minimum rating threshold (e.g. 7.5): ").strip())
                current_data = dh.get_movies_for_ratings(current_data, rating)
            except ValueError:
                print("Invalid rating; please enter a number like 7.5.")

        elif userIn == 5:
            short_data, full_data, analysis_string = dh.get_user_data_analysis(current_data)
            dh.export_data(full_data)
        
        elif userIn == 6:
            print("\nYou have selected option [{userIn}]: Get user data analysis. \n" \
                    "You will now see a summary of the data that you have filtered by. \n")
            analysis_data, full_data, analysis_string = dh.get_user_data_analysis(current_data)
            print(analysis_data.reset_index())
            print(analysis_string)
            continue_button = input("Enter any key to continue")

        else:
            print("Invalid selection please enter a number between1–4.")
            continue


        #Updating count to user to help guide decision making -> whether or not they should keep filtering
        count = len(current_data)
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
        print("\n🎬 Here's your final list:")
        print(current_data.copy().reset_index())

        print("\nHere is an analysis of the data that you have filtered by\n")
        analyzed_data, full_data, analysis_string = dh.get_user_data_analysis(current_data)
        print(analyzed_data.reset_index())
        print(analysis_string)

        dh.export_data(full_data)
    
if __name__ == '__main__':
    interactiveCLI()