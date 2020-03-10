import time
import pandas as pd
import numpy as np

# some comments are here

# some comments are here

# some comments are here

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    cities = {1:'chicago.csv', 2:'new_york_city.csv', 3:'washington.csv'}
    months = {0:'No filter', 1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June'}
    days = {0:'No filter', 1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday', 7:'Sunday'}
    
    print('Hello! Let\'s explore some US bikeshare data!')
    print('For all inputs, please enter approriate number from given options.')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = int(input('Would you like to see data for\n1. Chicago\n2. New York City\n3. Washington\n'))
        except:
            city = 4
        if city in range(1,4):
            break
        else:
            print('Please enter a valid input.')
            
    while True:
        try:
            fltr = int(input('Would you like to filter data by\n1. Month\n2. Day\n3. Not at all\n'))
        except:
            fltr = 4
        if fltr in range(1,4):
            break
        else:
            print('Please enter a valid input.')
    
    if fltr == 1:
        # get user input for month (all, january, february, ... , june)
        while True:
            try:
                month = int(input('Which month\n0. No filter\n1. January\n2. February\n3. March\n4. April\n5 .May\n6. June\n'))
            except:
                month = 7
            day = 0
            if month in range(1,7):
                break
            else:
                print('Please enter a valid input.')
            
    elif fltr == 2:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            try:
                day = int(input('Which day\n0. No filter\n1. Monday\n2. Tuesday\n3. Wednesday\n4. Thursday\n5. Friday\n6. Saturday\n7. Sunday\n'))
            except:
                day = 8
            month = 0
            if day in range(1,8):
                break
            else:
                print('Please enter a valid input.')
            
    elif fltr == 3:
        month = 0
        day = 0

    # converting to respective values
    city = cities[city]
    month = months[month]
    day = days[day]

    print('-'*40)
    return city, month, day


def display_raw_data(df):
    """Display raw data, 5 rows at a time."""
    rows = 0
    msg = ''
    while True:
        ans = input(f'Would you like to look at 5{msg} rows of raw data?(yes/no)')
        ans = ans.lower()
        if ans not in ['yes', 'no']:
            continue
        if ans == 'yes':
            print(df[rows:rows+5])
            rows += 5
            msg = ' more'
        else:
            return


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
    print('Trying to load data')
    try:
        df = pd.read_csv(city, index_col=0)
    except FileNotFoundError:
        print("File Not Found, Please make sure it is present in the same directory.")
        exit(1)
    print('Data loaded successsfully.')
    
    # necerray formatting
    df['Start Time'] =  pd.to_datetime(df['Start Time'])
    df['End Time'] =  pd.to_datetime(df['End Time'])
#     if 'Birth Year' in df.columns:
#         df['Birth Year'] = df['Birth Year'].fillna(df['Birth Year'].mode()[0]) # filling NaN values with mode of Birth Years
#         df['Birth Year'] = df['Birth Year'].astype(int)
    
    display_raw_data(df)
    print('We are going to perform some statistics now.')
    
    # adding extra helpful columns
    df['Month'] = df['Start Time'].dt.strftime('%B')
    df['Day'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour
    
    if month != 'No filter':
        df = df[df['Month'] == month]
    if day != 'No filter':
        df = df[df['Day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = df.groupby('Month').count()['Start Time'].idxmax()
    print(f'Most common month: {month}')


    # display the most common day of week
    day = df.groupby('Day').count()['Start Time'].idxmax()
    print(f'Most common day of week: {day}')

    # display the most common start hour
    hour = df.groupby('Hour').count()['Start Time'].idxmax()
    print(f'Most common hour of day: {hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df.groupby('Start Station').count()['Start Time'].idxmax()
    print(f'Most common start station: {start_station}')

    # display most commonly used end station
    end_station = df.groupby('End Station').count()['Start Time'].idxmax()
    print(f'Most common end station: {end_station}')

    # display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station','End Station'])['Start Time'].count().idxmax()
    print(f'Most common trip from start to end: {combination}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print(f'Total travel time: {total_time}')

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print(f'Mean travel time: {mean_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print('Counts of each user type:')
    print(user_type_counts)
    print()

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('Counts of each gender:')
        print(gender_counts)
        print()
    else:
        print('No Gender data to share.')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest Birth Year: ', int(df['Birth Year'].min()))
        print('Most recent Birth Year: ', int(df['Birth Year'].max()))
        print('Most common Birth Year: ', int(df['Birth Year'].mode()))
    else:
        print('No Birth Year data to share.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
