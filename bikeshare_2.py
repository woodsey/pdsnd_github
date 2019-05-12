import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_OPTIONS = ['january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december','all']
DAY_OPTIONS = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

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
    city,month,day='','',''
    while city.lower() not in CITY_DATA:
        city = input("specify a city to analyze (must be one of: Chicago, New York City, or Washington): ")

    # get user input for month (all, january, february, ... , june)
    while month.lower() not in MONTH_OPTIONS:
        month = input("Specify a month to view data for (or type all for the whole year): ")

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while day.lower() not in DAY_OPTIONS:
        day = input("Specify a day of the week to view data for (or type all for entire week): ")

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
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = (df.loc[df.month==(MONTH_OPTIONS.index(month)+1)])
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df.day_of_week==day.title()]

    print("We found a total of "+str(len(df.index))+" rides for your criteria:\n")
    print(" City: "+city.title()+"\n Month: "+month.title()+"\n Day: "+day.title())
    print('-'*40)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month=df['month'].mode().max()
    print(" Most common month: "+MONTH_OPTIONS[int(common_month)-1].title())

    # display the most common day of week
    common_day=df['day_of_week'].mode().max()
    print(" Most common day of week: "+common_day)

    # display the most common start hour
    common_hour=df['start_hour'].mode().max()
    print(" Most common start hour: "+str(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station=df.groupby(['Start Station']).size().reset_index()
    common_start_station.columns=['Start Station','Count']
    common_start_station=common_start_station.sort_values('Count',ascending=False)
    print(" Most common start station is '"+common_start_station.iloc[0,0]+"' with "+str(common_start_station.iloc[0,1])+" occurrences")

    # display most commonly used end station
    common_end_station=df.groupby(['End Station']).size().reset_index()
    common_end_station.columns=['End Station','Count']
    common_end_station=common_end_station.sort_values('Count',ascending=False)
    print(" Most common end station is '"+common_end_station.iloc[0,0]+"' with "+str(common_end_station.iloc[0,1])+" occurrences")

    # display most frequent combination of start station and end station trip
    common_start_end=df.groupby(['Start Station','End Station']).size().reset_index()
    common_start_end.columns=['Start Station','End Station','Count']
    common_start_end=common_start_end.sort_values('Count',ascending=False)
    print(" Most frequent combination of start and end station is '"+common_start_end.iloc[0,0]+"' and '"+common_start_end.iloc[0,1]+"' with "+str(common_start_end.iloc[0,2])+" occurrences")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel=df['Trip Duration'].sum()
    print(" Total travel time: "+str(int(int(total_travel/60)/60))+" hours")

    # display mean travel time
    mean_travel=df['Trip Duration'].mean()
    print(" Average trip duration: "+str(int(mean_travel/60))+" minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats... Please wait...\n')
    start_time = time.time()

    # Display counts of user types
    print(" Total of Subscribers and Customers:")
    user_types=df.groupby('User Type').size()
    print("  Customers: "+str(user_types['Customer']))
    print("  Subscribers: "+str(user_types['Subscriber']))

    if 'Gender' in df.columns:
        # Display counts of gender - only if that data exists
        print(" Total of Gender:")
        gender_types=df.fillna('Unspecified')
        gender_types=gender_types.groupby('Gender').size()

        print("  Male: "+str(gender_types['Male']))
        print("  Female: "+str(gender_types['Female']))
        print("  Unspecified: "+str(gender_types['Unspecified']))

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth - only if that data exists
        birth_years=df.sort_values(by=['Birth Year'], ascending=False)
        empty_birth_years=df['Birth Year'].isnull().sum()
        birth_years=birth_years.dropna(axis=0)
        print(" Birth years of users:")
        print("  Earliest birth year: "+str(int(birth_years['Birth Year'].min())))
        print("  Latest birth year: "+str(int(birth_years['Birth Year'].max())))
        print("  Average birth year: "+str(int(birth_years['Birth Year'].mode().max())))
        print("  Number of users with unspecificed birth year: "+str(empty_birth_years))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        # short cuts for testing:
#        city='chicago'
#        month='january'
#        day='all'
        city, month, day = get_filters()
        df = load_data(city.lower(), month.lower(), day.lower())
        if len(df.index)==0:
            print("There is no data for the options you've selected:\n City: "+city.title()+"\n Month: "+month.title()+"\n Day: "+day.title())
        else:
            show_sample=input("\nWould you like to see a sample of the data before we load the statistics (yes or no)?\n")
            if show_sample=='yes':
                start=0
                end=10
                keep_going=''
                while keep_going!='no':
                    print(df.iloc[start:end])
                    keep_going=input("\nWant to show another 10 lines of data (hit any key to continue, or type no to stop)?\n")
                    start+=10
                    end+=10

            print("\nLoading Statistics... Please wait...")
            print('-'*40)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        restart = input('\nWould you like to restart (yes, or any other key to exit)?.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
