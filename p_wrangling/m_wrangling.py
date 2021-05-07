# IMPORTS

from p_acquisition.m_acquisition import *
from datetime import datetime

# FUNCTIONS


def date_short(day, month, year):  # To put input date in useful format (text)
    short_month = month[0:3]
    date_format = f'{day} {short_month} {year}'
    return date_format


def date_for_weather(date):  # Puts the date in format readable by weather_df
    date_changed = datetime.strptime(date, "%d %b %Y").isoformat()
    weather_date = date_changed[:10]
    return weather_date


def get_df(list_of_lists):  # Return a dataframe from a list of lists given
    df_raw = pd.DataFrame(list_of_lists)
    return df_raw


def get_df_col(list_of_lists, cols):  # Return a dataframe from a list of lists given and columns names
    df_raw = pd.DataFrame(list_of_lists, columns=cols)
    return df_raw


def split_column(data_df, init_col, sep, first_col, sec_col):
    # Split a column in two by a separator, and add the new columns to the dataframe
    data_df[[first_col, sec_col]] = data_df[init_col].str.split(sep, expand=True)
    return data_df


def split_n(flight_list):  # Splits each element of a list by separator \n
    flight_list_clean = [x.split('\n') for x in flight_list]
    return flight_list_clean


def strip_str_col(data_df, column, to_remove):  # Clean elements of a column removing characters from the right
    data_df[column] = data_df[column].map(lambda x: x.rstrip(to_remove))
    return data_df


def get_code(table_df, row, column):  # Select a specific value from a table, considering the column and row given
    code_data = table_df.loc[row, column]
    return code_data


def get_row(table_df, column, data_code):  # Select a specific row from a table, considering the value in a column given
    row_wanted = table_df.loc[table_df[column] == data_code]
    return row_wanted


def get_value(data_ser, column):  # Select a specific value from a table of one row, considering the column given
    code = data_ser[column].values[0]
    return code


def get_destiny(flight_df, airports_df):  # Returns the variables city_name and country_name from the flight info
    city_code = get_code(flight_df,'iataCode','arrival')
    city_df = get_row(airports_df, 'iata_code', city_code)
    city_name = get_code(city_df, city_df.index[0], 'municipality')
    country_name = get_code(city_df, city_df.index[0], 'country_name')
    return city_name, country_name


def not_day(text):  # Return a string deleting the last word
    short_text = ' '.join(text.split(' ')[:-1])
    return short_text


def remove_empties(flight_list):  # Remove empty elements in a list
    flight_list_clean = [x for x in flight_list if x != ['']]
    return flight_list_clean


def apply_in_column(table_df, column, fun_to_apply):  # Apply a function to a dataframe column
    table_df[column] = table_df[column].apply(fun_to_apply)
    return table_df[column]


def transform_hour(hour):  # Transform string hour in datetime format
    hour_trf = datetime.strptime(hour, "%m/%d/%Y %I:%M %p")
    return hour_trf


def flight_serie(flight_df, date):  # Returns a df with only the row of the date requested
    flight_info = get_row(flight_df, 'Date', date)
    return flight_info


def get_flights_df_m1(flight_list, flight_cols):  # Return a dataframe with the information of all flights requested
    flight_df_raw = get_df(flight_list)
    flight_df_raw1 = split_column(flight_df_raw, 3, '(', 'Departure city', 'Departure code')
    flight_df_raw2 = split_column(flight_df_raw1, 4, '(', 'Arrival city', 'Arrival code')
    flight_df_raw3 = strip_str_col(flight_df_raw2, 'Departure code', ')')
    flight_df_raw4 = strip_str_col(flight_df_raw3, 'Arrival code', ')')
    flight_df_clean = flight_df_raw4[[2, 'Departure city', 'Departure code', 'Arrival city', 'Arrival code',5, 6, 7, 8, 9, 11]]
    flights_df = flight_df_clean.columns(flight_cols)
    return flights_df


def get_flights_df_m2(flight_list, flight_cols2, flight_cols_final):
    # Return a dataframe with the information of all flights requested
    flight_list_split = split_n(flight_list)
    flight_list_clean = remove_empties(flight_list_split)
    flight_df_raw = get_df_col(flight_list_clean, flight_cols2)
    flight_df_raw1 = split_column(flight_df_raw, 'Departure', '(', 'Departure city', 'Departure code')
    flight_df_raw2 = split_column(flight_df_raw1, 'Arrival', '(', 'Arrival city', 'Arrival code')
    flight_df_raw3 = strip_str_col(flight_df_raw2, 'Departure code', ')')
    flight_df_raw4 = strip_str_col(flight_df_raw3, 'Arrival code', ')')
    flights_df = flight_df_raw4[flight_cols_final]
    return flights_df


def flight_mode_selector(flight_list, flight_cols, flight_cols2):
    # Select how to clean the flight list depending on how it start
    if flight_list[0] == "":
        flight_df = get_flights_df_m1(flight_list, flight_cols2)
    else:
        flight_df = get_flights_df_m2(flight_list, flight_cols2, flight_cols)
    return flight_df


def get_flights_df(driver_route, flight_web, flight_code, flight_cols, flight_cols2, date_flight):
    # Returns the df with the flight information requested
    flight_list = get_flight_info(driver_route, flight_web, flight_code)
    flights_table = flight_mode_selector(flight_list, flight_cols, flight_cols2)
    flight_df = flight_serie(flights_table, date_flight)
    return flight_df


def currency_info(currency_table_route, departure_country, arrival_country):
    # Returns currency info of the country requested
    currency_df = get_df_from_csv(currency_table_route)
    departure_curr_df = get_row(currency_df, 'ENTITY', departure_country)
    departure_curr_code = get_value(departure_curr_df, 'Alphabetic Code')
    arrival_curr_df = get_row(currency_df, 'ENTITY', arrival_country)
    arrival_curr_code = get_value(arrival_curr_df, 'Alphabetic Code')
    arrival_curr_name = get_value(arrival_curr_df, 'Currency')
    return departure_curr_code, arrival_curr_code, arrival_curr_name


def hour_diff_calculate(route, web, departure_timezone, arrival_timezone):
    # Returns the hour difference between the two zones entered
    if (departure_timezone == 0) | (arrival_timezone == 0):
        hour_diff = 'No'
    else:
        departure_h, arrival_h = get_tz_dif(route, web, departure_timezone, arrival_timezone)
        departure_hour = transform_hour(departure_h)
        arrival_hour = transform_hour(arrival_h)
        difference = arrival_hour - departure_hour
        hour_diff = difference.total_seconds() / 60**2
    return hour_diff


def weather_info(date, weather_df):  # Collect weather info of the flight date in arrival city
    date_weather = date_for_weather(date)
    weather_day_df = get_row(weather_df, 'datetime', date_weather)
    temp = get_value(weather_day_df, 'temp')
    max_temp = get_value(weather_day_df, 'max_temp')
    min_temp = get_value(weather_day_df, 'min_temp')
    rain = get_value(weather_day_df, 'pop')
    snow = get_value(weather_day_df, 'snow')
    humidity = get_value(weather_day_df, 'rh')
    clouds = get_value(weather_day_df, 'clouds')
    return temp, max_temp, min_temp, rain, snow, humidity, clouds

