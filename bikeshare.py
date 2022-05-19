import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAY_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def convert_sec(sec):
    """
    Converts seconds in hour, minutes, seconds.
    
    Args:
        (int) sec - sum of seconds to be converted 
    
    Returns:
        (int) hours
        (int) minutes
        (int) remaining seconds
    """
    
    hours = int(sec / 3600)
    minutes = int((sec % 3600) / 60)
    seconds = int(sec % 60)
    
    return '{} hours {} minutes {} seconds'.format(hours, minutes, seconds)


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
        #until a valid city is entered it will raise an value error
        try:
            city = input('Please choose one of the following cities (Chicago, New York City or Washington): \n').lower()
            if city not in CITY_DATA:
                raise ValueError
        except ValueError:
            print('\n"{}" is not a valid city!'.format(city))
        else:
            break
        
    # get user input for month (all, january, february, ..., june)
    while True:
        #until a valid month is entered it will raise an value error
        try:
            month = input('\nPlease choose a month from January to June or "all" if you don\'t want a Month filter: \n').lower()
            if month not in MONTH_DATA:
                raise ValueError
        except ValueError:
            print('\n"{}" is not a valid month!'.format(month))
        else:
            break
        
    # get user input for day of week (all, monday, tuesday, ..., sunday)
    while True:
        #until a valid day is entered it will raise an value error
        try:
            day = input('\nPlease choose a day of the week (e.g. "monday") or "all" if you don\'t want a day filter: \n').lower()
            if day not in DAY_DATA:
                raise ValueError
        except ValueError:
            print('\n"{}" is not a valid day!'.format(day))
        else:
            break
    
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
    print('>>> Loading choosen data...city: {}, month: {}, day: {} <<<'.format(city, month, day))
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
   
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int (Jan = 1, Feb = 2,..., Jun = 6)
        month = MONTH_DATA.index(month)
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    # filter by day of week if applicable (Mon = 1,..., Sun = 7)
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df_month = df.groupby(['month'])['Start Time'].count()
    print('- The most common month by number of trips is {}, with a total of {}.'.format(MONTH_DATA[df_month.idxmax()].title(), df_month.max()))
    
    # display the most common day of week
    df_day = df.groupby(['day_of_week'])['Start Time'].count()
    print('- The most common day of the week by number of trips is {}, with a total of {}.'.format(df_day.idxmax(), df_day.max()))

    # display the most common start hour
    df_hour = df.groupby(df['Start Time'].dt.hour)['Start Time'].count()
    print('- The most common start hour for trips is {}, with a total of {}.'.format(df_hour.idxmax(), df_hour.max()))

    
    # time to calculate
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trips."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    df_start = df.groupby(['Start Station'])['Start Station'].count()
    print('- The most commonly used start station is {}, with a total of {}.'.format(df_start.idxmax(), df_start.max()))
    #print(df_start)
    
    # display most commonly used end station
    df_end = df.groupby(['End Station'])['End Station'].count()
    print('- The most commonly used end station is {}, with a total of {}.'.format(df_end.idxmax(), df_end.max()))
    #print(df_end)

    # display most frequent combination of start station and end station trip
    df_combi = df.groupby(['Start Station','End Station'])['Start Station'].count()
    print('- With {} trips, the most frequent combination is to start at {} and to finish at {}.'.format(df_combi.max(), df_combi.idxmax()[0], df_combi.idxmax()[1]))
    
    # time to calculate
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    X = np.array(df['Trip Duration'])
    print('- The total travel time for your choosen selection is:', convert_sec(X.sum()))
    
    # display mean travel time
    print('- The mean travel time for your choosen selection is:', convert_sec(X.mean()))    
 
    # time to calculate
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df.groupby(['User Type'])['User Type'].count(), '\n')
    
    # Display counts of gender und birth data
    if city in 'washington':
        # for Washington there are no gender and birth data, so this must be handled
        print('Sorry, no gender and birth data available for Washington.')
    else:
        # Display counts of gender
        print(df.groupby(['Gender'])['Gender'].count(), '\n')

        # Display earliest, most recent, and most common year of birth
        # drop NaN rows from birth data
        df_birth = df['Birth Year'].dropna(axis = 0)
        X = np.unique(df_birth, return_counts=True)
       
        print('- The earliest birth year is {}.'.format(int(np.min(X[0]))))
        print('- The youngest person is born in {}.'.format(int(np.max(X[0]))))
        print('- The most common birth year is {}.'.format(int(df_birth.mode()[0])))

        
    # time to calculate
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def raw_data(df):
    """Displays raw data line by line as long as the user want or until end of data"""
    
    # if user input is y = yes and it is not the end of the df, raw data shown line by line
    answer = input('\nDo you want to see trip details, please enter "y" ?\n').lower()
    n = 0
    while answer == 'y' and n < len(df):
        print(df.iloc[n])
        n += 1
        if n < len(df):
            answer = input('\nContinue with "y".\n').lower() 
        else:
            print('\nNo. {} was the last record!'.format(n))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
