import time

import numpy as np
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    valid_city = False
    while not valid_city:
        city = input ("Please specify either Chicago, New York City or Washington:\n").title()
        if city not in ("Chicago","New York City","Washington"):
            print ("You did not enter a valid city.")
        else:
            valid_city = True

    # get user input for month (all, january, february, ... , june)
    month = ""
    valid_month = False
    while not valid_month:
        month = input ("Please specify a month between January and June, or 'All' to see data for all 6 months:\n").title()
        if month not in ("All","January","February","March","April","May","June"):
            print ("You did not enter a valid month.")
        else:
            valid_month = True

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    valid_day = False
    while not valid_day:
        day = input ("Please specify a day of the week between Sunday and Saturday, or 'All' to see data for all days:\n").title()
        if day not in ("All","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"):
            print ("You did not enter a valid day.")
        else:
            valid_day = True

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    if city == "Chicago":
        filename = "chicago.csv"
    elif city == "New York City":
        filename = "new_york_city.csv"
    else:
        filename = "washington.csv"
    
    df = pd.read_csv(filename)
    original = df.copy()

    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # Extract month and day from 'Start Time' and add as new columns
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    df["Month"] = df["Start Time"].apply(lambda x: months[x.month - 1])
    df["Day"] = df["Start Time"].dt.weekday_name

    # Filter by month
    if month != "All":
        df = df[df['Month'] == month]

    # Filter by day
    if day != "All":
        df = df[df['Day'] == day.title()]
       
    return df, original


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most common month: ", df['Month'].mode().to_string(index = False))

    # display the most common day of week
    print("Most common day of week: ", df['Day'].mode().to_string(index = False))

    # display the most common start hour
    df["Hour"] = df["Start Time"].dt.hour
    print("Most common start hour: ", df['Hour'].mode().to_string(index = False))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print ("Most commonly used start station: ", df['Start Station'].mode().to_string(index = False))

    # display most commonly used end station
    print ("Most commonly used end station: ", df['End Station'].mode().to_string(index = False))

    # display most frequent combination of start station and end station trip
    start_end = df["Start Station"].combine(df["End Station"], lambda s1, s2: "START = " + s1 + ", END = " + s2)
    print ("Most frequent combination of start station and end station trip: ",start_end.mode().to_string(index = False))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_hours = df['Trip Duration'].sum() / 360
    print ("Total travel time: " + str(round(total_hours, 1)) + " hours")

    # display mean travel time
    mean_minutes = df['Trip Duration'].mean() / 60
    print ("Mean travel time: " + str(round(mean_minutes, 1)) + " minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print ("Counts of user types:")
    print ("=====================")
    print (df.groupby(["User Type"])["User Type"].count().to_string())

    # Display counts of gender
    if city != "Washington":
        print ("\nCounts of gender:")
        print ("===================")
        print (df.groupby(["Gender"])["Gender"].count().to_string())
    else:
        print ("\nGender counts are not available for this city.")

    # Display earliest, most recent, and most common year of birth
    if city != "Washington":
        print ("\nEarliest year of birth: ", int(df['Birth Year'].min()))
        print ("Most recent year of birth: ", int(df['Birth Year'].max()))
        print ("Most common year of birth: ", df['Birth Year'].mode().to_string(index = False, float_format = "%4.0f"))
    else:
        print ("Year of birth data are not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        
        df, original = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        rawdata = input("\nWould you like to see the raw data? Enter Yes or No.\n")
        if rawdata.title() == "Yes":
            counter = 0
            for row in range(original.shape[0]):
                if counter < 5:
                    result = original.iloc[[row]].to_dict("records")
                    for key, value in result[0].items():
                        print (str(key) + ":" + str(value))
                    print ()
                    counter += 1
                else:
                    cont = input ("\nWould you like to see further raw data? Enter Yes or No.\n")
                    if cont.title() != "Yes":
                        break
                    counter = 0

        restart = input('\nWould you like to restart? Enter Yes or No.\n')
        if restart.title() != "Yes":
            break

if __name__ == "__main__":
	main()
