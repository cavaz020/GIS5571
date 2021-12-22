import pandas as pd

# -------Functions for Cleaning Flight Data----------------------------


def keep_two_cols(month):
    # Creating a dataframe with only the airport name and the total number of flights that arrived
    month_total_flights = month[['airport', 'airport_name', 'arr_flights']]
    return month_total_flights


def correct_type(month_total_flights):
    # Converting the datatype of the airport name to string
    month_total_flights['airport_name'] = month_total_flights['airport_name'].astype(
        'string')
    return month_total_flights


def create_state_list(month_total_flights):
    # Looping through the airport name column and extracting the state abbreviations
    # Putting the state abbreviations into a list
    state_list = []
    for i in month_total_flights['airport_name']:
        comma_position = i.find(',')
        state_1 = i[comma_position+2]
        state_2 = i[comma_position+3]
        state_both = state_1 + state_2
        state_list.append(state_both)
    return state_list


def create_col(month_total_flights, state_list):
    # Creating a new column in the dataframe to hold the state abbreviation
    month_total_flights['state_abbrev'] = state_list
    return month_total_flights


def agg_by_airport(data_frame):
    # Returns a dataframe of the data grouped and summed by airport
    grouped_airport_df = data_frame.groupby(
        ['airport', 'airport_name', 'state_abbrev']).sum()
    return grouped_airport_df


def export_df_as_csv(month_total_flights, month_of_interest_str):
    # Exporting the Dataframe as a CSV
    path_name = ('/Users/cavazosarte/projects/GIS5571/Final_Project/' +
                 month_of_interest_str + '.csv')
    exported_csv = month_total_flights.to_csv(path_name)
    return exported_csv

# ------------Functions for aggregating data by state------------------


def agg_by_state(data_frame):
    # Returns a dataframe of the data grouped and summed by state
    grouped_state_df = data_frame.groupby(['state_abbrev']).sum()
    return grouped_state_df


# ----------CLEANING MONTHLY FLIGHT DATA----------------
# March Functions
march = pd.read_csv(
    '/Users/cavazosarte/projects/GIS5571/Final_Project/MARCH_AIRPORT_DATA.csv')
march_clean = keep_two_cols(march)
correct_type(march_clean)
march_list = create_state_list(march_clean)
march_clean = create_col(march_clean, march_list)
march_clean = agg_by_airport(march_clean)
export_df_as_csv(march_clean, 'march')

# April Functions
april = pd.read_csv(
    '/Users/cavazosarte/projects/GIS5571/Final_Project/APRIL_AIRPORT_DATA.csv')
april_clean = keep_two_cols(april)
correct_type(april_clean)
april_list = create_state_list(april_clean)
april_clean = create_col(april_clean, april_list)
april_clean = agg_by_airport(april_clean)
april_clean = agg_by_airport(april_clean)
export_df_as_csv(april_clean, 'april')

# May Functions
may = pd.read_csv(
    '/Users/cavazosarte/projects/GIS5571/Final_Project/MAY_AIRPORT_DATA.csv')
may_clean = keep_two_cols(may)
correct_type(may_clean)
may_list = create_state_list(may_clean)
may_clean = create_col(may_clean, may_list)
may_clean = agg_by_airport(may_clean)
export_df_as_csv(may_clean, 'may')

# June Functions
june = pd.read_csv(
    '/Users/cavazosarte/projects/GIS5571/Final_Project/JUNE_AIRPORT_DATA.csv')
june_clean = keep_two_cols(june)
correct_type(june_clean)
june_list = create_state_list(june_clean)
june_clean = create_col(june_clean, june_list)
june_clean = agg_by_airport(june_clean)
export_df_as_csv(june_clean, 'june')


# July Functions
july = pd.read_csv(
    '/Users/cavazosarte/projects/GIS5571/Final_Project/JULY_AIRPORT_DATA.csv')
july_clean = keep_two_cols(july)
correct_type(july_clean)
july_list = create_state_list(july_clean)
july_clean = create_col(july_clean, july_list)
july_clean = agg_by_airport(july_clean)
export_df_as_csv(july_clean, 'july')


# August Functions
august = pd.read_csv(
    '/Users/cavazosarte/projects/GIS5571/Final_Project/AUG_AIRPORT_DATA.csv')
aug_clean = keep_two_cols(august)
correct_type(aug_clean)
aug_list = create_state_list(aug_clean)
aug_clean = create_col(aug_clean, aug_list)
aug_clean = agg_by_airport(aug_clean)
export_df_as_csv(aug_clean, 'august')


# ---------------------FLIGHT DATA BY STATE-----------------
# March
# Reading the csv in as a dataframe
march_state_df = pd.read_csv(
    '/Users/cavazosarte/projects/GIS5571/Final_Project/march.csv')
march_flights_state = agg_by_state(march_state_df)
export_df_as_csv(march_flights_state, 'march_flights_by_state')
# April
april_state_df = pd.read_csv(
    '/Users/cavazosarte/projects/GIS5571/Final_Project/april.csv')
april_flights_state = agg_by_state(april_state_df)
export_df_as_csv(april_flights_state, 'april_flights_by_state')
# May
may_state_df = pd.read_csv(
    '/Users/cavazosarte/projects/GIS5571/Final_Project/may.csv')
may_flights_state = agg_by_state(march_state_df)
export_df_as_csv(may_flights_state, 'may_flights_by_state')
# June
june_state_df = pd.read_csv(
    '/Users/cavazosarte/projects/GIS5571/Final_Project/june.csv')
june_flights_state = agg_by_state(june_state_df)
export_df_as_csv(june_flights_state, 'june_flights_by_state')
# July
july_state_df = pd.read_csv(
    '/Users/cavazosarte/projects/GIS5571/Final_Project/july.csv')
july_flights_state = agg_by_state(july_state_df)
export_df_as_csv(july_flights_state, 'july_flights_by_state')
# August
aug_state_df = pd.read_csv(
    '/Users/cavazosarte/projects/GIS5571/Final_Project/august.csv')
aug_flights_state = agg_by_state(aug_state_df)
export_df_as_csv(aug_flights_state, 'aug_flights_by_state')
