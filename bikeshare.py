import time
import pandas as pd

# FIX 1: Removed unused numpy import

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS   = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city  - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day   - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # FIX 5: All inputs already use .lower().strip() and re-prompt on invalid entry
    while True:
        city = input('Enter city (chicago, new york city, washington): ').lower().strip()
        if city in CITY_DATA:
            break
        print('Invalid city. Please choose from: chicago, new york city, washington.')

    while True:
        month = input('Enter month (all, january, february, ..., june): ').lower().strip()
        if month == 'all' or month in MONTHS:
            break
        print('Invalid month. Please enter "all" or a month from january to june.')

    while True:
        day = input('Enter day of week (all, monday, tuesday, ..., sunday): ').lower().strip()
        if day == 'all' or day in DAYS:
            break
        print('Invalid day. Please enter "all" or a day name (e.g. monday).')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city  - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day   - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month']      = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour']       = df['Start Time'].dt.hour

    if month != 'all':
        df = df[df['month'] == MONTHS.index(month) + 1]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    # FIX 6: Guard against empty dataframe before calling mode()
    if df.empty:
        print('No data available to compute time statistics.')
        return

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print('Most Common Month:', MONTHS[common_month - 1].title())

    common_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', common_day.title())

    common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    # FIX 6: Guard against empty dataframe before calling mode()
    if df.empty:
        print('No data available to compute station statistics.')
        return

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('Most Commonly Used Start Station:', df['Start Station'].mode()[0])

    print('Most Commonly Used End Station:', df['End Station'].mode()[0])

    combo = (df['Start Station'] + ' --> ' + df['End Station']).mode()[0]
    print('Most Frequent Trip:', combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    # FIX 6: Guard against empty dataframe before calling sum()/mean()
    if df.empty:
        print('No data available to compute trip duration statistics.')
        return

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_seconds = df['Trip Duration'].sum()
    print('Total Travel Time: {} seconds ({:.2f} hours)'.format(
        int(total_seconds), total_seconds / 3600))

    mean_seconds = df['Trip Duration'].mean()
    print('Mean Travel Time: {:.2f} seconds ({:.2f} minutes)'.format(
        mean_seconds, mean_seconds / 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    # FIX 6: Guard against empty dataframe before calling value_counts()/mode()
    if df.empty:
        print('No data available to compute user statistics.')
        return

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('Counts of User Types:')
    print(df['User Type'].value_counts().to_string())

    # FIX 7: Washington safety — Gender and Birth Year columns may not exist
    if 'Gender' in df.columns:
        print('\nCounts of Gender:')
        print(df['Gender'].value_counts().to_string())
    else:
        print('\nGender data not available for this city.')

    if 'Birth Year' in df.columns:
        print('\nEarliest Birth Year:   ', int(df['Birth Year'].min()))
        print('Most Recent Birth Year:', int(df['Birth Year'].max()))
        print('Most Common Birth Year:', int(df['Birth Year'].mode()[0]))
    else:
        print('Birth year data not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Offers the user a chance to view 5 rows of raw data at a time."""
    i = 0
    # FIX 4: Loop only while rows remain; prevents infinite loop and index overflow
    while i < len(df):
        # FIX 3: Validate input — only accept 'yes' or 'no', re-prompt otherwise
        while True:
            show = input('\nWould you like to see 5 rows of raw data? Enter yes or no.\n').lower().strip()
            if show in ['yes', 'no']:
                break
            print('Invalid input. Please enter yes or no.')

        if show == 'no':
            break

        print(df.iloc[i:i + 5].to_string())
        i += 5

        if i >= len(df):
            print('No more data to display.')
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # FIX 2: Handle empty dataframe — inform user and skip statistics
        if df.empty:
            print('\nNo data available for the selected filters. Please try different options.')
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df)

        # FIX 5: Validate restart prompt — only accept 'yes' or 'no'
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower().strip()
            if restart in ['yes', 'no']:
                break
            print('Invalid input. Please enter yes or no.')

        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
