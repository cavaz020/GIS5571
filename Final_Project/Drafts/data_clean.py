import pandas as pd
import numpy as np


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

# ------------Functions for aggregating data by state and county------------------


def agg_by_state(data_frame):
    # Returns a dataframe of the data grouped and summed by state
    grouped_state_df = data_frame.groupby(['state_abbrev']).sum()
    return grouped_state_df


def agg_by_county(data_frame):
    # Returns a dataframe of the data grouped and summed by state and county
    # Grouped by two columns because some county names repeat in different states
    grouped_county_df = data_frame.groupby(
        ["STATE", "COUNTY", 'arr_flights']).sum()
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


def create_state_list_dems(data_frame):
    state_list = []
    for i in data_frame['NAME']:
        n = i.index(',')
        state_list.append(i[n+2:])
    return state_list


def turn_into_abbreviation(state_list):
    abbreviations_dict = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
                          'Montana': 'MT', 'Nebraska': 'NE',  'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'}
    state_abbrev_list = []
    for i in state_list:
        if i in abbreviations_dict.keys():
            state_abbrev_list.append(abbreviations_dict[i])
    return state_abbrev_list


def add_county_name_col(data_frame, county_list):
    # Function to add a column to the dataframe holding all of the county names
    data_frame['COUNTY'] = county_list
    return data_frame


def add_state_name_col(data_frame, state_abbrev_list):
    data_frame['STATE'] = state_abbrev_list
    return data_frame


def create_sum_col(data_frame):
    # Function to create a column holding the sum of all of the columns
    # of people who have identified in any way as 'American Indian and Alaska Native'
    # or 'Native Hawaiian and other Pacific Islander'
    # And naming this column 'TOTAL_NATIVE'
    data_frame = data_frame.rename(columns={'P1_001N': 'TOTAL_POP'})
    col_list = data_frame.columns.tolist()
    data_frame['TOTAL_POP'] = data_frame['TOTAL_POP'].apply(pd.to_numeric)
    keep_list = ['GEO_ID', 'NAME', 'TOTAL_POP', 'P1_005N', 'STATE', 'COUNTY']
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
# # March Functions
# march = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/MARCH_AIRPORT_DATA.csv')
# march_clean = keep_two_cols(march)
# correct_type(march_clean)
# march_list = create_state_list(march_clean)
# march_clean = create_col(march_clean, march_list)
# march_clean = agg_by_airport(march_clean)
# export_df_as_csv(march_clean, 'march')

# # April Functions
# april = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/APRIL_AIRPORT_DATA.csv')
# april_clean = keep_two_cols(april)
# correct_type(april_clean)
# april_list = create_state_list(april_clean)
# april_clean = create_col(april_clean, april_list)
# april_clean = agg_by_airport(april_clean)
# april_clean = agg_by_airport(april_clean)
# export_df_as_csv(april_clean, 'april')

# # May Functions
# may = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/MAY_AIRPORT_DATA.csv')
# may_clean = keep_two_cols(may)
# correct_type(may_clean)
# may_list = create_state_list(may_clean)
# may_clean = create_col(may_clean, may_list)
# may_clean = agg_by_airport(may_clean)
# export_df_as_csv(may_clean, 'may')

# # June Functions
# june = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/JUNE_AIRPORT_DATA.csv')
# june_clean = keep_two_cols(june)
# correct_type(june_clean)
# june_list = create_state_list(june_clean)
# june_clean = create_col(june_clean, june_list)
# june_clean = agg_by_airport(june_clean)
# export_df_as_csv(june_clean, 'june')


# # July Functions
# july = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/JULY_AIRPORT_DATA.csv')
# july_clean = keep_two_cols(july)
# correct_type(july_clean)
# july_list = create_state_list(july_clean)
# july_clean = create_col(july_clean, july_list)
# july_clean = agg_by_airport(july_clean)
# export_df_as_csv(july_clean, 'july')


# # August Functions
# august = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/AUG_AIRPORT_DATA.csv')
# aug_clean = keep_two_cols(august)
# correct_type(aug_clean)
# aug_list = create_state_list(aug_clean)
# aug_clean = create_col(aug_clean, aug_list)
# aug_clean = agg_by_airport(aug_clean)
# export_df_as_csv(aug_clean, 'august')


# ---------------------FLIGHT DATA BY STATE-----------------
# # March
# # Reading the csv in as a dataframe
# march_state_df = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/march.csv')
# march_flights_state = agg_by_state(march_state_df)
# export_df_as_csv(march_flights_state, 'march_flights_by_state')
# # April
# april_state_df = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/april.csv')
# april_flights_state = agg_by_state(april_state_df)
# export_df_as_csv(april_flights_state, 'april_flights_by_state')
# # May
# may_state_df = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/may.csv')
# may_flights_state = agg_by_state(march_state_df)
# export_df_as_csv(may_flights_state, 'may_flights_by_state')
# # June
# june_state_df = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/june.csv')
# june_flights_state = agg_by_state(june_state_df)
# export_df_as_csv(june_flights_state, 'june_flights_by_state')
# # July
# july_state_df = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/july.csv')
# july_flights_state = agg_by_state(july_state_df)
# export_df_as_csv(july_flights_state, 'july_flights_by_state')
# # August
# aug_state_df = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/august.csv')
# aug_flights_state = agg_by_state(aug_state_df)
# export_df_as_csv(aug_flights_state, 'aug_flights_by_state')

# ----------------NUMBER OF AIRPORTS BY STATE------------------
# airports = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/Airport_points.csv')
# airports.dropna(subset=['State_Post_Office_Code'], inplace=True)
# data = [airports['State_Post_Office_Code']]
# header = ['STATE']
# airport_states = pd.concat(data, axis=1, keys=header)
# num_airports_state = airport_states.groupby(
#     ['STATE']).size().reset_index(name='airport_count')
# export_df_as_csv(num_airports_state, 'airport_count_by_state')

# ---------------NUMBER OF AIRPORTS BY COUNTY------------------
# airports = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/Airport_points.csv')

# data = [airports['County'], airports['State_Post_Office_Code']]
# header = ['COUNTY', 'STATE']
# airport_counties = pd.concat(data, axis=1, keys=header)
# num_airports_county = airport_counties.groupby(
#     ['COUNTY', 'STATE']).size().reset_index(name='airport_count')
# export_df_as_csv(num_airports_county, 'airport_count_by_county')

# ---------------AIRPORT NAME BY COUNTY----------------------------
# airports = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/Airport_points.csv')
# county_fips = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/county_fips_USDA.csv')
# county_fips['Name'] = county_fips['Name'].str.upper()
# # print(county_fips.head())
# data = [airports['County'], airports['State_Post_Office_Code'],
#         airports['Loc_Id'], airports['Fac_Name']]
# header = ['COUNTY', 'STATE', 'AIRPORT_ABBREV', 'AIRPORT_NAME']
# airport_and_county = pd.concat(data, axis=1, keys=header)
# # print(airport_and_county.head())
# county_fips_list = []
# airport_and_county['FIPS'] = np.nan
# for i in airport_and_county.index:
#     temp_state_df = county_fips[(
#         county_fips["State"] == airport_and_county['STATE'][i])]
#     for p in temp_state_df.index:
#         if temp_state_df['Name'][p] == airport_and_county['COUNTY'][i]:
#             airport_and_county['FIPS'][i] = temp_state_df['FIPS'][p]
# export_df_as_csv(airport_and_county, 'airport_and_county_names')

# ----------------COVID BY STATE----------------------------------------
# # March
# march_covid = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/covid_by_state_march_days.csv')
# march_covid = march_covid.groupby(
#     ['state']).sum()
# export_df_as_csv(march_covid, 'covid_by_state_march')

# # April
# april_covid = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/covid_by_state_april_days.csv')
# april_covid = april_covid.groupby(
#     ['state']).sum()
# export_df_as_csv(april_covid, 'covid_by_state_april')

# # May
# may_covid = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/covid_by_state_may_days.csv')
# may_covid = may_covid.groupby(
#     ['state']).sum()
# export_df_as_csv(may_covid, 'covid_by_state_may')

# # June
# june_covid = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/covid_by_state_june_days.csv')
# june_covid = june_covid.groupby(
#     ['state']).sum()
# export_df_as_csv(june_covid, 'covid_by_state_june')

# # July
# july_covid = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/covid_by_state_july_days.csv')
# july_covid = july_covid.groupby(
#     ['state']).sum()
# export_df_as_csv(july_covid, 'covid_by_state_july')

# # August
# aug_covid = read_csv(
#     '/Users/cavazosarte/projects/GIS5571/Final_Project/covid_by_state_aug_days.csv')
# aug_covid = aug_covid.groupby(
#     ['state']).sum()
# export_df_as_csv(aug_covid, 'covid_by_state_aug')

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
# # Creating a list of the states without the counties
# states = create_state_list_dems(new_header_race_data)
# # Transforming the states into abbreviation format
# states_abbrev = turn_into_abbreviation(states)
# # Creating a column in the dataframe of the states
# county_native_data = add_state_name_col(new_header_race_data, states_abbrev)
# # Creating a column in the dataframe of the counties in uppercase letters
# # This column will be used to join to the census shapefile
# county_native_data = add_county_name_col(new_header_race_data, counties)
# # Creating a column of the sum of all of the people in that county that identified as native
# county_native_data_sum = create_sum_col(county_native_data)
# # Exporting the cleaned csv for use in arcgis pro
# export_df_as_csv(county_native_data_sum, 'native_pop')
all_covid = pd.read_csv(
    '/Users/cavazosarte/projects/GIS5571/Final_Project/covid_cases_by_state_march_aug.csv')
# print(all_covid.head())
# march = []
# april = []
# may = []
# june = []
# july = []
# august = []
# months_num_list = ['03', '04', '05', '06', '07', '08']
# for i in all_covid['submission_date']:
#     if '03/' in i:
#         march.append(all_covid['submission_date'][i].index)
# print(march)

# index = all_covid.index
# condition = 3 in all_covid["submission_date"] and 
# apples_indices = index[condition]
# apples_indices_list = apples_indices.tolist()
# print(apples_indices_list)
