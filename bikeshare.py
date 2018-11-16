import time
import datetime
import pandas as pd
import numpy as np

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
    while True:
        city = input("\nWould you like to see data from Chicago, New York, or Washington?\n").lower()
        if city in ("chicago", "washington"):
            break
        elif city == "new york":
            city = "new york city"
            break
        else:
            print("\nThe city name is not present in the list")
    while True:
        sel = input('\nWould you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.\n').lower()
        if sel in ("month", "day", "both", "none"):
            break
        else:
            print("\nYou have not entered a valid filter")  

    # get user input for month (all, january, february, ... , june)
    if sel == "month" or sel == "both":
        while True:
            month = input("\nWhich month? January, February, March, April, May, or June?\n").title()
            if month in ('January', 'February', 'March', 'April', 'May', 'June'):
                break
            else:
                print("\nThe month name is not present in the list")
    else:
        month = "all"
       
    # get user input for day of week (all, monday, tuesday, ... sunday)
    if sel == "day" or sel == "both":
        while True:
            day = input("\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday?\n").title()
            if day in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday'):
                break
            else:
                print("\nThe day name inserted is not correct")
    else:
        day = "all"
       
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
            'Sunday']
        day = days.index(day)
        df = df.loc[df['day_of_week'] == day]


    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # display the most common month
    if len(df['Start Time'].dt.month.unique()) > 1:
        print('Most Popular Month: ', months[df['Start Time'].dt.month.mode()[0] - 1])

    # display the most common day of week
    if len(df['Start Time'].dt.dayofweek.unique()) > 1:
        print('Most Popular Month: ', days[df['Start Time'].dt.dayofweek.mode()[0]])

    # display the most common start hour
    print('Most Popular Start Hour: ', df['Start Time'].dt.hour.mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Popular Start Station: ', df['Start Station'].mode()[0])


    # display most commonly used end station
    print('Most Popular End Station: ', df['End Station'].mode()[0])


    # display most frequent combination of start station and end station trip
    df['Trip'] = df['End Station'] + ", " + df['End Station']
    print('Most Popular Combination Of Start Station And End Station Trip: ', df['Trip'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The Total Travel Time is: ', str(datetime.timedelta(seconds = int(df['Trip Duration'].sum()))))


    # display mean travel time
    print('The Mean Travel Time is: ', str(datetime.timedelta(seconds = int(df['Trip Duration'].mean()))))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    try:
        # Display counts of user types
        print('The Counts Of User Types is:\nSubscribers: {}\nCustomers: {}'.format(df['User Type'].value_counts().values[0], df['User Type'].value_counts().values[1]))

        # Display counts of gender
        print('The Counts Of User Gender is:\nMale: {}\nFemale: {}'.format(df['Gender'].value_counts().values[0], df['Gender'].value_counts().values[1]))

        # Display earliest, most recent, and most common year of birth
        print('The Earliest Year Of Birth is: ', int(df['Birth Year'].min()))
        print('The Most Recent Year Of Birth is: ', int(df['Birth Year'].max()))
        print('The Most Common Year Of Birth is: ', int(df['Birth Year'].mode()[0]))
    
    except:
        print("No user data for Washington City")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    start_row = 0
    end_row = 5
    while True:
        start = input('\nDo you want to see raw data? Enter yes or no.\n')
        if start.lower() != 'yes':
            break
        else:
            print(df.iloc[start_row : end_row , 0 : len(df.columns) - 3])
        while df.shape[0] > end_row:
            restart = input('\nDo you want to see more 5 lines of raw data? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
            else:
                start_row += 5
                end_row += 5
                print(df.iloc[start_row : end_row , 0 : len(df.columns) - 3])
        break     
            
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__== "__main__":
	main()
 