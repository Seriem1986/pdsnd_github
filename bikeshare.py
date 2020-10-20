# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 12:05:21 2020

@author: TIMWEGN
"""
import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#User input validation lists
valid_cities = ["chicago", "new york city", "washington"]
valid_months = ["all", "january", "february", "march", "april", "may", "june"]
valid_days = ["all", "monday","tuesday","wednesday","thuesday","friday","saturday","sunday"]

#Change to test mode
test_mode = False

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    #User texts
    usr_err_str_default = "The {} you enterd are not in the data or is misspelled! Please enter again\n"
    usr_str_city = "Would you like to see data for Chicago, New York City or Washington?\n"
    usr_err_str_city = usr_err_str_default.format("city")
    usr_str_month = "Which month? (all, january, february, march, april, may, june)\n"
    usr_err_str_month = usr_err_str_default.format("month")
    usr_str_day = "Which day? (all, monday, tuesday, wednesday, thuesday, friday, saturday, sunday)\n"
    usr_err_str_day = usr_err_str_default.format("day")

    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). 
    # HINT: Use a while loop to handle invalid inputs
    user_input_city = "nan"
    while user_input_city not in valid_cities:
        user_input_city = input(usr_str_city).strip().lower()
        if user_input_city not in valid_cities:
            print(usr_err_str_city)

    # TO DO: get user input for month (all, january, february, ... , june)
    user_input_month = "nan"
    while user_input_month not in valid_months:
        print(usr_str_month)        
        user_input_month = input().strip().lower()
        if user_input_month not in valid_months:
            print(usr_err_str_month)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    user_input_day = "nan"
    while user_input_day not in valid_days:
        user_input_day = input(usr_str_day).strip().lower()
        if user_input_day not in valid_days:
            print(usr_err_str_day)

    if user_input_city == "new york city":
        user_input_city = "new_york_city"

    print('-'*40)
    return user_input_city, user_input_month, user_input_day

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

    df = pd.read_csv("{}.csv".format(city))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by day of week
    if day != 'all':
        # set the day filter and create new df
        df = df[df['day_of_week'] == day.title()]

    # filter by month
    if month != 'all':
        months = ["january", "february", "march", "april", "may", "june"]
        month_index = months.index(month) + 1
        # filter the month and create the new df
        df = df[df['month'] == month_index]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    try:

        # TO DO: display the most common month
        if not df['month'].empty:
            common_month = df['month'].mode()[0]
            print('Most common start month:', common_month)
        else:
            print('For this month are no data available')

        # TO DO: display the most common day of week
        if not df['day_of_week'].empty:
            common_day = df['day_of_week'].mode()[0]
            print('Most common start hour:', common_day)
        else:
            print('For this day are no data available')

        # TO DO: display the most common start hour
        if not df['hour'].empty:
            common_hour = df['hour'].mode()[0]
            print('Most common start hour:', common_hour)
        else:
            print('For this hour are no data available')

    except:
        print("Something unexpected happend. Sorry :(")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    if not df['Start Station'].empty:
        start_station_list_sorted = df['Start Station'].value_counts().sort_values(ascending=False)
        most_usd_start_station = start_station_list_sorted.index[0]
        print("Most commonly used start station is:\n\"{}\"".format(most_usd_start_station))
    else:
        print("There are no start station data avalable!")

    # TO DO: display most commonly used end station
    if not df['End Station'].empty:
        end_station_list_sorted = df['End Station'].value_counts().sort_values(ascending=False)
        most_usd_end_station = end_station_list_sorted.index[0]
        print("Most commonly used end station is:\n\"{}\"".format(most_usd_end_station))
    else:
        print("There are no end station data avalable!")

    # TO DO: display most frequent combination of start station and end station trip
    if not df['End Station'].empty and not df['Start Station'].empty:
        df_comb = df['Start Station'] + " --> " + df['End Station']
        df_comb_sorted = df_comb.value_counts().sort_values(ascending=False)
        most_usd_combined_station = df_comb_sorted.index[0]
        print("Most frequent combination of start station and end station is:\n\"{}\"".format(most_usd_combined_station))
    else:
        print("There are no end to end station data avalable!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if not df['Trip Duration'].empty:
        # TO DO: display total travel time
        total_travel_time = int(df['Trip Duration'].sum())
        usr_str_totaltraveltime = "The total travel time was {}".format(total_travel_time)
        print(usr_str_totaltraveltime)

        # TO DO: display mean travel time        
        mean_travel_time = int(df['Trip Duration'].mean())
        usr_str_meantraveltime = "The mean travel time was {}\n".format(mean_travel_time)
        print(usr_str_meantraveltime)
    else:
        print("Could not calculate travel date because there are no data")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()
    print('\nLets see what we konw about our users!')
    print('\n')
    try:
        # TO DO: Display counts of user types
        if not df['User Type'].empty:
            print("That is the distribution from user typ")
            print(df['User Type'].value_counts())
            print('\n')

        # TO DO: Display counts of gender
        if not df['Gender Type'].empty:
            print("That is the distribution from user gender")
            print(df['Gender'].value_counts())
            print('\n')

        # TO DO: Display earliest, most recent, and most common year of birth
        if not df['Birth Year'].empty:
            print("And here some other intersessting Data!")
            # NOTE: Drop the data which have no information
            birth_year_max = int(df['Birth Year'].dropna(axis = 0).max())
            birth_year_min = int(df['Birth Year'].dropna(axis = 0).min())
            birth_year_mostcommon = int(df['Birth Year'].dropna(axis = 0).mode())

            print('\n')
            
            print("Most recent year of birth: {}".format(birth_year_max))
            print("Earliest year of birth: {}".format(birth_year_min))
            print("Most common year of birth: {}".format(birth_year_mostcommon))

    except:
        print("Not all Data for this time available!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    #row counter for display next 5 lines
    row_counter = 0
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        while True:
            individual = input('\nWould you like to view individual trip data? Enter yes or no.\n')
            if individual.lower() != 'yes':
                break

            if row_counter >= df.count()[0]:
                print("you reach the end of the data")
                break
            index = row_counter
            print(df.iloc[index,:])
            print(df.iloc[index + 1,:])
            print(df.iloc[index + 2,:])
            print(df.iloc[index + 3,:])
            print(df.iloc[index + 4,:])
            print(df.iloc[index + 5,:])
            print(df.iloc[index + 6,:])
            print(df.iloc[index + 7,:])
            row_counter += 8

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

def test():
    """Test all the input the user can make."""
    testloop = 0
    result = ""
    for city in valid_cities:
        if city == "new york city":
            city = "new_york_city"
        for month in valid_months:
            for day in valid_days:
                exception_counter = 0
                testloop +=1
                test_parameter = "{}-{}-{}".format(city, month, day)
                try:
                    df = load_data(city, month, day)
                    time_stats(df)
                    station_stats(df)
                    trip_duration_stats(df)
                    user_stats(df)
                except:
                    exception_counter +=1
                    result += "Testloop {} - NOK\n".format(testloop)
                    result += "Test parameter: {}\n".format(test_parameter)
                    result += "\n"
    print(result)

if __name__ == "__main__":
    if test_mode:
        test()
    else:
        main()





