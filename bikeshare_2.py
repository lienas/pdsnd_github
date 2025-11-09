"""Bikeshare data analysis tool.

This module analyzes bikeshare data from Chicago, New York City, and Washington.
It provides interactive filtering and statistical analysis of trip data including
time patterns, station usage, trip duration, and user demographics.
"""

import time
import pandas as pd


CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}


def get_filters():
    """Ask user to specify a city, month, and day to analyze.

    Returns:
        tuple: A tuple containing (city, month, day) as strings where:
            city - name of the city to analyze (chicago, new york city, washington)
            month - name of the month to filter by, or "all" for no filter
            day - name of the day of week to filter by, or "all" for no filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = input("Enter city name (chicago, new york city, washington): ").lower()
    while city not in CITY_DATA:
        city = input("Invalid city: type one of (chicago, new york city, washington)").lower()

    month = input("Enter month name (all, january, february, ... , june): ").lower()
    months = ['all', 'january', 'february', 'march', 'april',
              'may', 'june']
    while month not in months:
        month = input("Invalid month: type one of (all, january, february, ... , june)").lower()

    day = input("Enter day of week (all, monday, tuesday, ... , sunday): ").lower()
    days = ['all', 'monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']
    while day not in days:
        day = input("Invalid day: type one of (all, monday, tuesday, ... , sunday)").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """Load data for the specified city and apply month and day filters.

    Args:
        city (str): Name of the city to analyze
        month (str): Name of the month to filter by, or "all" for no month filter
        day (str): Name of the day of week to filter by, or "all" for no day filter

    Returns:
        pandas.DataFrame: Bikeshare data filtered by month and day with additional
            computed columns: month, day_of_week, and hour
    """
    df = pd.read_csv(CITY_DATA[city])

    start_time = pd.to_datetime(df['Start Time'])
    df['month'] = start_time.dt.month_name().str.lower()
    df['day_of_week'] = start_time.dt.day_name().str.lower()
    df['hour'] = start_time.dt.hour

    if month != 'all':
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Display statistics on the most frequent times of travel.

    Calculates and prints the most common month, day of week, and hour
    from the provided bikeshare data.

    Args:
        df (pandas.DataFrame): Bikeshare data containing month, day_of_week, and hour columns
    """
    print('\nCalculating Most Frequent Times of Travel...\n')
    start_time = time.time()

    print(f'Most common month: {df["month"].mode()[0]}')
    print(f'Most common day: {df["day_of_week"].mode()[0]}')
    print(f'Most common hour: {df["hour"].mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Display statistics on the most popular stations and trip.

    Calculates and prints the most common start station, end station,
    and start/end station combination from the provided bikeshare data.

    Args:
        df (pandas.DataFrame): Bikeshare data containing Start Station and End Station columns
    """
    print('\nCalculating Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('Most common start station:',
          df['Start Station'].mode()[0])
    print('Most common end station:',
          df['End Station'].mode()[0])

    combo = df.groupby(['Start Station',
                        'End Station']).size().idxmax()
    print('Most common start/end combination:', combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration.

    Calculates and prints the total and mean trip duration in a
    human-readable format (days, hours, minutes, seconds).

    Args:
        df (pandas.DataFrame): Bikeshare data containing Trip Duration column in seconds
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total = df['Trip Duration'].sum()
    d = int(total // 86400)
    h = int((total % 86400) // 3600)
    m = int((total % 3600) // 60)
    s = int(total % 60)
    print(f'Total: {d}d {h}h {m}m {s}s')

    mean = df['Trip Duration'].mean()
    d = int(mean // 86400)
    h = int((mean % 86400) // 3600)
    m = int((mean % 3600) // 60)
    s = int(mean % 60)
    print(f'Mean: {d}d {h}h {m}m {s}s')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Display statistics on bikeshare users.

    Calculates and prints counts of user types, gender distribution (if available),
    and birth year statistics (if available) from the provided bikeshare data.

    Args:
        df (pandas.DataFrame): Bikeshare data containing User Type column and
            optionally Gender and Birth Year columns
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print(f'User types:\n{user_types}')
    print('-'*40)

    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(f'Gender:\n{gender}')
        print('-'*40)
    else:
        print('Gender data not available')

    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode()[0])

        print('Birth year stats')
        print('-'*20)
        print(f'Earliest: {earliest}')
        print(f'Most recent: {recent}')
        print(f'Most common: {common}')
    else:
        print('Birth year data not available')

    print('-'*40)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Display raw data in chunks of 5 rows upon user request.

    Continuously prompts the user if they want to see 5 more rows of raw data
    until they decline or all data has been displayed.

    Args:
        df (pandas.DataFrame): Bikeshare data to display
    """
    start_idx = 0
    chunk_size = 5

    while start_idx < len(df):
        show_data = input('\nWould you like to see 5 rows of raw data? Enter yes/no.\n')
        if show_data.lower() != 'yes':
            break

        end_idx = min(start_idx + chunk_size, len(df))
        print(df.iloc[start_idx:end_idx])
        start_idx = end_idx

        if start_idx >= len(df):
            print('\nNo more data to display.')


def main():
    """Execute the main program loop for bikeshare data analysis.

    Prompts user for filters, loads and analyzes data, displays statistics,
    and allows the user to restart the analysis with different filters.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nRestart? Enter yes/no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
