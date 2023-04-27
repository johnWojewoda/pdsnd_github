import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
Asks users to specify a city, month and day to analyze.

Creates a function that creates a tuple with three elements: city, month, and day. This tuple is then returned by the function and is stored in a variable and used directly in other parts of the program.
    """
    # The first thing we do is print an initial statement
    print('Hello there! Let\'s explore some US bikeshare data!') # using the escape character so ' should be treated specifically
   
    while True: # sets a while loop that will run indefinitely until a break statement is encountered.
        cities= ['chicago','new york city','washington']
         # get user input for city.
        city= input("\n Which cities data set would you like to analyse? (Chicago, New york city, Washington) \n").lower() # .lower()ensures lower case.
        if city in cities:
            break # if input is correct, move to next command
        else:
            print("\n Please enter a valid city name")    


    # gets the user input for the month 
    while True:
        months= ['January','February','March','April','June','May','None']
        month = input("\n Which of the following months would you like to examine? (January, February, March, April, May, June)? Type 'None' for no month filter\n").title()
        if month in months:
            break
        else:
            print("\n Please enter a valid month")    


    # gets user input for day of week 
    while True:
        days= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','None']
        day = input("\n Which day of the week would you like to consider? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)? Type 'None' for no day filter \n").title()         
        if day in days:
            break
        else:
            print("\n Please enter a valid day")    
    

    # separate the sections with 40 - hyphens
    print('-'*40)
    # returns a tuple
    return city, month, day


def load_data(city, month, day):
    """
        The load_data() function expects three arguments, which will be passed as a tuple when the function is called. The function then unpacks the tuple into separate variables city, month, and day, which it uses to filter the data accordingly. 
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day      
    """

    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    # dt.weekday_name has been deprecated
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'None':
        # use the index of the months list to get the corresponding month
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month)+1 # adds 1 to compensate for 0 base
    
        # filter by month to create the new dataframe
        df = df[df['month']==month] 

    # filter by day of week if applicable
    if day != 'None':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day]

    return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month =='None':
        pop_month= df['month'].mode()[0]
        months= ['January','February','March','April','May','June']
        pop_month= months[pop_month-1]
        print("The most Popular month is",pop_month)


    # display the most common day of week
    if day =='None':
        pop_day= df['day_of_week'].mode()[0]
        print("The most Popular day is",pop_day)


    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    pop_hour=df['Start Hour'].mode()[0]
    print("The popular Start Hour is {}:00 hrs".format(pop_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start_station= df['Start Station'].mode()[0]
    print("The most commonly used Start Station is {}".format(pop_start_station))


    # display most commonly used end station
    pop_end_station= df['End Station'].mode()[0]
    print("The most commonly used End Station is {}".format(pop_end_station))

    # display most frequent combination of start station and end station trip
    df['combination']=df['Start Station']+" "+"to"+" "+ df['End Station']
    pop_com= df['combination'].mode()[0]
    print("The most frequent combination of Start and End Station is {} ".format(pop_com))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time() # uses the time module

    # display total travel time
    total_duration=df['Trip Duration'].sum()
    minute,second=divmod(total_duration,60) # Uses divmod function to covert seconds to hours, minutes and seconds
    hour,minute=divmod(minute,60)
    print("The total trip duration: {} hour(s) {} minute(s) {} second(s)".format(hour,minute,second))
    
    # display mean travel time
    average_duration=round(df['Trip Duration'].mean())
    m,sec=divmod(average_duration,60)
    if m>60:
        h,m=divmod(m,60)
        print("The total trip duration: {} hour(s) {} minute(s) {} second(s)".format(h,m,sec))
    else:
        print("The total trip duration: {} minute(s) {} second(s)".format(m,sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts= df['User Type'].value_counts()
    print("The user types are:\n",user_counts)


    # Display counts of gender
    if city.title() == 'Chicago' or city.title() == 'New York City':
        gender_counts= df['Gender'].value_counts()
        print("\nThe counts of each gender are:\n",gender_counts)
    
    # Display earliest, most recent, and most common year of birth
        earliest= int(df['Birth Year'].min())
        print("\nThe oldest user is born of the year",earliest)
        most_recent= int(df['Birth Year'].max())
        print("The youngest user is born of the year",most_recent)
        common= int(df['Birth Year'].mode()[0])
        print("Most users are born of the year",common)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):

    while True:
        response=['yes','no']
        choice= input("Would you like to view individual trip data (5 entries)? Type 'yes' or 'no'\n").lower()
        if choice in response:
            if choice=='yes':
                start=0
                end=5
                data = df.iloc[start:end,:9]
                print(data)
            break     
        else:
            print("Please enter a valid response")
    if  choice=='yes':       
            while True:
                choice_2= input("Would you like to view more trip data? Type 'yes' or 'no'\n").lower()
                if choice_2 in response:
                    if choice_2=='yes':
                        start+=5
                        end+=5
                        data = df.iloc[start:end,:9]
                        print(data)
                    else:    
                        break  
                else:
                    print("Please enter a valid response")              


def main(): # Called by the 'if__name__== "__main__":' idiom. Creates an indefinite loop that only breaks when restart response is not yes
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__": # sometimes called the 'main guard' or 'main check'
	main()
    
# I need cite the work of ABDALLAH EL-SAWY whoes work helped me greatly. After attempting this myself, finding this web page online https://www.kaggle.com/code/abdallahmohamedamin/explore-us-bikeshare-data/notebook helped me understand this code. This, in conjunction with GhatGPT has made it so that I understand the conepts behind every line of the above code.
