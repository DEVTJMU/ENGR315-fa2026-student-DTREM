import sys

"""
Create a program which will provide answers to the questions posed in the assignment description.
We've provided a function which will parse the NYT covid database file (named "us-counties.csv"); 
however, its correct implementation will be up to you. DO NOT MODIFY THIS FUNCTION.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
"""


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information

    ____________________ DO NOT MODIFY THIS FUNCTION ___________________
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

### YOUR CODE HERE ###
"""
When was the first positive COVID case in Harrisonburg? (FIPS code 51660)
When was the first positive case in Rockingham County? (Rockingham County)
On what date was the greatest number of new cases reported in Harrisonburg? 
What date in Rockingham County?
What was the worst seven-day period in Harrisonburg city for new COVID cases? 
What period in Rockingham County? These are the seven-day periods when the number of new cases was maximal.
"""
### YOUR CODE HERE ###

from pathlib import Path
from datetime import datetime


# 1. Get the directory of the current script
script_dir = Path(__file__).resolve().parent

# Go up TWO directories
grandparent_dir = script_dir.parent.parent

# Construct path from there
target_file = grandparent_dir / "data" / "covid" / "us-counties.csv"

# Parse the NYT COVID data file into a list of tuples
raw_data = parse_nyt_data(target_file)

# Define functions to extract daily new cases for specific locations
def get_daily_new_cases(data, fips):
    """
    Build the daily new case series for one place.

    The NYT data stores cumulative cases
    calculate new cases by subtracting the 
    previous day's cumulative total from the
    current day's cumulative total.

    :param data: list of tuples from parse_nyt_data
    :param fips: FIPS code identifying the place
    :return: list of (date, new_cases) tuples in date order
    """

    # Store only the records for the requested location.
    location_data = []

    # Loop through all entries and collect those matching the FIPS code
    for entry in data:
        (date, county, state, entry_fips, cases, deaths) = entry
        
        # Check if the FIPS code matches the requested location
        if entry_fips == fips:
            location_data.append((date, cases))

    # The NYT data normally already in date order, but sorting
    # makes the function work correctly regardless of input order.
    location_data.sort()

    # compute the daily new cases from the cumulative data
    daily = []

    # If there is no data for this location, return an empty list immediately
    if len(location_data) == 0:
        return daily

    # For the first day, the number of new cases is the cumulative
    # number reported on that day.
    previous_cases = 0

    # Loop through the location data and calculate new cases for each day
    for date, cumulative_cases in location_data:

        # Calculate new cases for the current day based on the previous day's cumulative cases
        new_cases = cumulative_cases - previous_cases

        # Occasionally cumulative COVID data can be corrected downward.
        # do not want a negative correction to count as "new cases."
        if new_cases < 0:
            new_cases = 0

        # Append the calculated new cases for the current day to the daily list
        daily.append((date, new_cases))
        # Update the previous day's cumulative cases for the next iteration
        previous_cases = cumulative_cases

    return daily

# Define functions to extract daily new cases for specific counties
def get_daily_new_cases_by_county(data, county):
    """
    Build the daily new-case series for a county.

    :param data: list of tuples from parse_nyt_data
    :param county: county name
    :return: list of (date, new_cases) tuples in date order
    """

    location_data = []

    # Loop through all entries and collect those matching the county name in Virginia
    for entry in data:
        (date, entry_county, state, fips, cases, deaths) = entry

        #  get the correct county in Virginia.
        if entry_county == county and state == 'Virginia':
            location_data.append((date, cases))

    # At this point, location_data contains all the cumulative case counts for the specified county in Virginia
    location_data.sort()

    daily = []

    # If there is no data for this county, return an empty list immediately
    if len(location_data) == 0:
        return daily

    previous_cases = 0

    for date, cumulative_cases in location_data:

        new_cases = cumulative_cases - previous_cases

        if new_cases < 0:
            new_cases = 0

        # Append the calculated new cases for the current day to the daily list
        daily.append((date, new_cases))

        previous_cases = cumulative_cases

    return daily

# Define functions to analyze daily new cases
def first_case_date(daily):
    """
    Return the first date on which new COVID cases were reported.
    """
    # Loop through the daily new cases and return the first date with new cases
    for date, new_cases in daily:
        if new_cases > 0:
            return date

    return None

# Define a function to find the worst single day of new cases
def worst_day(daily):
    """
    Return (date, new_cases) for the largest single day.
    """
    # If there is no data, return None immediately
    if len(daily) == 0:
        return None

    # Initialize the worst day with the first entry in the daily list   
    worst_date = daily[0][0]
    worst_cases = daily[0][1]

    # Loop through the daily new cases to find the worst day
    for date, new_cases in daily:
        # Check if the current day's new cases exceed the worst cases found so far
        if new_cases > worst_cases:
            worst_date = date
            worst_cases = new_cases

    # Return the worst day found
    return (worst_date, worst_cases)


# Define a function to find the worst week of new cases
def worst_week(daily):
    """
    Return (start_date, end_date, total) for the seven-day period
    containing the greatest total number of new cases.

    Each window contains seven consecutive days.
    """
    # If there are fewer than seven days of data, return None immediately
    if len(daily) < 7:
        return None

    # Initialize variables to track the worst week
    worst_start = None
    worst_end = None
    worst_total = None

    # Check every possible seven-day window in the daily data.
    for i in range(len(daily) - 6):

        # Determine the start and end dates for the current seven-day window
        start_date = daily[i][0]
        end_date = daily[i + 6][0]

        # Initialize the total number of new cases for the current window
        total = 0

        # Sum the new cases for the current seven-day window
        for j in range(i, i + 7):
            total += daily[j][1]

        # Update the worst week if the current window has a higher total than the previous worst
        if worst_total is None or total > worst_total:
            worst_total = total
            worst_start = start_date
            worst_end = end_date

    return (worst_start, worst_end, worst_total)

######### HBURG #########

# Harrisonburg City has FIPS code 51660.
harrisonburg_daily = get_daily_new_cases(raw_data, '51660')

harrisonburg_first_case = first_case_date(harrisonburg_daily)
harrisonburg_worst_day = worst_day(harrisonburg_daily)
harrisonburg_worst_week = worst_week(harrisonburg_daily)

######### ROCKINGHAM COUNTY #########

rockingham_daily = get_daily_new_cases_by_county(raw_data, 'Rockingham')

rockingham_first_case = first_case_date(rockingham_daily)
rockingham_worst_day = worst_day(rockingham_daily)
rockingham_worst_week = worst_week(rockingham_daily)

######### PRINT THE ANSWERS #########

print()
print("COVID-19 Analysis")
print("-----------------")

print("Harrisonburg:")
print("First positive case:", harrisonburg_first_case)

if harrisonburg_worst_day is not None:
    print("Greatest number of new cases in one day:",
          harrisonburg_worst_day[0],
          "with",
          harrisonburg_worst_day[1],
          "new cases")

if harrisonburg_worst_week is not None:
    print("Worst seven-day period:",
          harrisonburg_worst_week[0],
          "through",
          harrisonburg_worst_week[1],
          "with",
          harrisonburg_worst_week[2],
          "new cases")


print()
print("Rockingham County:")
print("First positive case:", rockingham_first_case)

if rockingham_worst_day is not None:
    print("Greatest number of new cases in one day:",
          rockingham_worst_day[0],
          "with",
          rockingham_worst_day[1],
          "new cases")

if rockingham_worst_week is not None:
    print("Worst seven-day period:",
          rockingham_worst_week[0],
          "through",
          rockingham_worst_week[1],
          "with",
          rockingham_worst_week[2],
          "new cases")