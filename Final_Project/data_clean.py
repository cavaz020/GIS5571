import pandas as pd


def read_csv(file_path):
    # Importing CSV
    month = pd.read_csv(file_path)
    return month

# -------Functions for Cleaning Flight Data----------------------------


def keep_two_cols(month):
    # Creating a dataframe with only the airport name and the total number of flights that arrived
    month_total_flights = month[['airport', 'airport_name', 'arr_flights']]
    return month_total_flights


def correct_type(month_total_flights):
    # Converting the datatype of the airport name to string
    month_total_flights['airport_name'] = month_total_flights['airport_name'].astype(
        'string')


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
    # Creating a new column in the database to hold the state abbreviation
    month_total_flights['state_abbrev'] = state_list
    return month_total_flights


def export_df_as_csv(month_total_flights, month_of_interest_str):
    # Exporting the Dataframe as a CSV
    path_name = ('/Users/cavazosarte/projects/GIS5571/Final_Project/' +
                 month_of_interest_str + '.csv')
    exported_csv = month_total_flights.to_csv(path_name)
    return exported_csv

# ------------Functions for aggregating data by state and county------------------


def agg_by_state(data_frame):
    # Returns a dataframe of the data grouped and summed by state
    grouped_state_df = data_frame.groupby(['state_abbrev']).sum()
    return grouped_state_df


def agg_by_county(data_frame):
    # Returns a dataframe of the data grouped and summed by county
    grouped_county_df = data_frame.groupby(['County']).sum()
    return grouped_county_df

# ------------Functions for Cleaning Census Data-------------------------------------


def col_names_to_list(data_frame):
    # Function to get a list of the column header names
    col_names_list = data_frame.loc[0, :].values.tolist()
    return col_names_list


def get_only_native_data(col_list):
    # Function to create a list of column indices without data on native population
    nonnative_cols = []
    word = 'Native'
    for i in col_list:
        if word not in i:
            nonnative_cols.append(col_list.index(i))
    return nonnative_cols


def create_native_df(data_frame, col_list):
    # Function to create dataframe by removing the columns without data on native people
    keep_list = [0, 1, 2]
    for i in keep_list:
        str(i)
        col_list.remove(i)
    only_native_data = data_frame.drop(data_frame.columns[col_list], axis=1)
    return only_native_data


def alter_header(data_frame):
    # Function to remove the first row of metadata from the csv and reset the index at 0
    data_frame = data_frame.drop([0])
    data_frame = data_frame.reset_index()
    data_frame = data_frame.iloc[:, 1:]
    return data_frame


def create_county_list(data_frame):
    # Function to create a list of county names in all caps without state and comma
    county_list = []
    for i in data_frame['NAME']:
        i = i.upper()
        n = i.index(',')
        county_list.append(i[:n])
    return county_list


def add_county_name_col(data_frame, county_list):
    # Function to add a column to the dataframe holding all of the county names
    data_frame['COUNTY'] = county_list
    return data_frame


def create_sum_col(data_frame):
    # Function to create a column holding the sum of all of the columns
    # of people who have identified in any way as 'American Indian and Alaska Native'
    # or 'Native Hawaiian and other Pacific Islander'
    # And naming this column 'TOTAL_NATIVE'
    data_frame = data_frame.rename(columns={'P1_001N': 'TOTAL_POP'})
    col_list = data_frame.columns.tolist()
    data_frame['TOTAL_POP'] = data_frame['TOTAL_POP'].apply(pd.to_numeric)
    keep_list = ['GEO_ID', 'NAME', 'TOTAL_POP', 'P1_005N', 'COUNTY']
    for i in keep_list:
        col_list.remove(i)
    data_frame['P1_005N'] = data_frame['P1_005N'].apply(pd.to_numeric)
    sum_column = data_frame['P1_005N']
    for col in col_list:
        data_frame[col] = data_frame[col].apply(pd.to_numeric)
        sum_column = sum_column + data_frame[col]
    data_frame["TOTAL_NATIVE"] = sum_column
    return data_frame

# ----------CLEANING MONTHLY FLIGHT DATA----------------
# March Functions
# march = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/MARCH_AIRPORT_DATA.csv')
# march_clean = keep_two_cols(march)
# correct_type(march_clean)
# march_list = create_state_list(march_clean)
# march_clean = create_col(march_clean, march_list)
# export_df_as_csv(march_clean, 'march')

# # April Functions
# april = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/APRIL_AIRPORT_DATA.csv')
# april_clean = keep_two_cols(april)
# correct_type(april_clean)
# april_list = create_state_list(april_clean)
# april_clean = create_col(april_clean, april_list)
# export_df_as_csv(april_clean, 'april')

# # May Functions
# may = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/MAY_AIRPORT_DATA.csv')
# may_clean = keep_two_cols(may)
# correct_type(may_clean)
# may_list = create_state_list(may_clean)
# may_clean = create_col(may_clean, may_list)
# export_df_as_csv(may_clean, 'may')

# # June Functions
# june = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/JUNE_AIRPORT_DATA.csv')
# june_clean = keep_two_cols(june)
# correct_type(june_clean)
# june_list = create_state_list(june_clean)
# june_clean = create_col(june_clean, june_list)
# export_df_as_csv(june_clean, 'june')


# ---------------------FLIGHT DATA BY STATE-----------------
# March
# Reding the csv in as a dataframe
march_state_df = read_csv(
    '/Users/cavazosarte/projects/GIS5571/Final_Project/march.csv')
march_flights_state = agg_by_state(march_state_df)
export_df_as_csv(march_flights_state, 'march_flights_by_state')
# April
april_state_df = read_csv(
    '/Users/cavazosarte/projects/GIS5571/Final_Project/april.csv')
april_flights_state = agg_by_state(april_state_df)
export_df_as_csv(april_flights_state, 'april_flights_by_state')
# May
may_state_df = read_csv(
    '/Users/cavazosarte/projects/GIS5571/Final_Project/may.csv')
may_flights_state = agg_by_state(march_state_df)
export_df_as_csv(may_flights_state, 'may_flights_by_state')
# June
june_state_df = read_csv(
    '/Users/cavazosarte/projects/GIS5571/Final_Project/june.csv')
june_flights_state = agg_by_state(june_state_df)
export_df_as_csv(june_flights_state, 'june_flights_by_state')

# ----------------CLEANING RACE CENSUS DATA-------------
# # Reading in the csv of 'Race' from the 2020 Census
# race_data = read_csv(
#     'county_census_data_race.csv')
# # Creating a list of the values in the first row (metadata)
# race_col_list = col_names_to_list(race_data)
# # Creating a list of columns containing data on non-native race identified people
# non_native_cols = get_only_native_data(race_col_list)
# # Creating a dataframe of only columns containing data on native race identified people
# native_data_df = create_native_df(race_data, non_native_cols)
# # Removing the row of metadata from the dataframe
# new_header_race_data = alter_header(native_data_df)
# # Creating a list of the counties without the state on the end
# counties = create_county_list(new_header_race_data)
# # Creating a column in the dataframe of the counties in uppercase letters
# # This column will be used to join to the census shapefile
# county_native_data = add_county_name_col(new_header_race_data, counties)
# # Creating a column of the sum of all of the people in that county that identified as native
# county_native_data_sum = create_sum_col(county_native_data)
# # Exporting the cleaned csv for use in arcgis pro
# export_df_as_csv(county_native_data_sum, 'native_pop')
