import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months_list = ['january', 'february', 'march', 'april', 'may', 'june', "all"]
days_list = ['Monday', 'Tuesday', 'Wednesday',
             'Thursday', 'Friday', 'Saturday', 'Sunday', "All"]

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
    #Initializing an empty city var to store user city selection
    city = ''
    city = input('which city do you want to display? please enter[chicago or new york city or washington]: ').lower()
    while city not in CITY_DATA.keys():
        print(f"The city you entered {city} is a wrong value, please try again")
        city = input('which city do you want to display? please enter[chicago or new york city or washington]: ').lower()

    # get user input for month (all, january, february, ... , june)
    month = ''
    month = input('which month do you want to display? if you don\'t want to filter by month please enter all: ').lower()
    while month.lower() not in months_list:
        print(f"The month you entered {month} is a wrong value, please try again")
        month = input(
            'which month do you want to display? if you don\'t want to filter by month please enter all: ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    day = input('which day do you want to display? if you don\'t want to filter by day please enter all: ').lower()
    while day.title() not in days_list:
        print(f"The day you entered {day} is a wrong value, please try again")
        day = input(
            'which day do you want to display? if you don\'t want to filter by day please enter all: ').lower()


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
    print("\nLoading data")
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # adding two columns month and day of the week
    df['month'] = df['Start Time'].dt.month
    df['day of the week'] = df['Start Time'].dt.day_name()
    
     # filter data by month and day
    if month != "all":
        month = months_list.index(month)+1
        df = df[df['month'] == month]

    if day.title() != "All":
        df = df[df['day of the week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_popular_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('Most Popular Month:', months[most_popular_month-1])
  
    # display the most common day of week
    print('the most Frequent day of the week of Travel is: ',
          df['day of the week'].mode()[0])
    # display the most common start hour
    print('the most Frequent hour of Travel is: ',
          df['Start Time'].dt.hour.mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

   # display most commonly used start station
    print('the most Popular start Station is: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('the most Popular end Station is: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['start and end station combination'] = df['Start Station'] + \
        " to "+df['End Station']
    print('the most Popular combination of start and end Stations is: ',
          df['start and end station combination'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('the total travel time is: ', df['Trip Duration'].sum(), "seconds")
    # display mean travel time
    print('the average travel time is: ', df['Trip Duration'].mean(), "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print(user_types, "\n")
    
    # Display counts of gender 
    if 'Gender' not in df.columns:
        print('this city selected has no gender stats')
    else:
        gender_stats = df.groupby(['Gender'])['Gender'].count()
        print(gender_stats)
    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        print('this city has no birthyear stats')
    else:
        print('the earliest year of birth is: \n', int(df['Birth Year'].min()))
        print('the most recent year of birth is: \n',
              int(df['Birth Year'].max()))
        print('the most common year of birth is: \n',
              int(df['Birth Year'].mode()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_data(df):
    answer = input("would you like to see 5 rows of data? enter yes or no: ").lower()
    start_row = 0
    while answer == "yes":
        print(df.iloc[start_row:start_row+5])
        start_row += 5
        answer = input("would you like to see more 5 rows of data? enter yes or no: ").lower()


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
            print("Thank you for using bikeshare")
            break


if __name__ == "__main__":
	main()
