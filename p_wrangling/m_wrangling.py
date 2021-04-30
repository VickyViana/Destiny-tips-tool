# IMPORTS

import pandas as pd
import re
from p_acquisition.m_acquisition import *
from datetime import datetime
from datetime import date

# FUNCTIONS


def date_short(day, month, year):  # To put input date in useful format (text)
    short_month = month[0:3]
    date_format = f'{day} {short_month} {year}'
    return date_format


def date_for_weather(date): # Puts the date in format readable by weather_df
    date_changed = datetime.strptime(date, "%d %b %Y")
    weather_date = date(date_changed).isoformat()
    return weather_date


def make_sublist(list_raw, n_components):  # Divide a list in a list of lists of n components
    list_of_lists = [list_raw[x:x + n_components] for x in range(0, len(list_raw), n_components)]
    return list_of_lists


def get_df(list_of_lists, cols):  # Return a dataframe from a list of lists given
    df_raw = pd.DataFrame(list_of_lists, columns=cols)
    return df_raw


def split_column(data_df, init_col, sep, first_col, sec_col):  # Split a column in two by a separator, and add the new columns to the dataframe
    data_df[[first_col, sec_col]] = data_df[init_col].str.split(sep, expand=True)
    return data_df


def split_n(flight_list):  # Splits each element of a list by separator \n
    flight_list_clean = [x.split('\n') for x in flight_list]
    return flight_list_clean


def strip_str_col(data_df, column, to_remove):  # Clean elements of a column removing characters from the right
    data_df[column] = data_df[column].map(lambda x: x.rstrip(to_remove))
    return data_df


def get_code(table_df, row, column):
    code_data = table_df.loc[row, column]
    return code_data


def get_row(table_df, column, data_code):
    row_wanted = table_df.loc[table_df[column] == data_code]
    return row_wanted


def get_value(data_serie, column):
    code = data_serie[column].values[0]
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


def only_num(text):  # Return ony the numbers in a string
    result = (re.findall('\d+', text))
    return ''.join(result)


def remove_empties(flight_list):
    flight_list_clean = [x for x in flight_list if x != ['']]
    return flight_list_clean


def apply_in_column(table_df, column, fun_to_apply):  # Apply a function to a dataframe column
    table_df[column] = table_df[column].apply(fun_to_apply)
    return table_df[column]


def transform_hour(hour):
    hour_trf = datetime.strptime(hour, "%m/%d/%Y %I:%M %p")
    return hour_trf


def clean_weather(weather_df):  # To clean weather_df columns, to have more useful values
    weather_df['Forecast'] = apply_in_column(weather_df, 'Forecast', not_day)
    weather_df['High temperature (ºC)'] = apply_in_column(weather_df, 'High temperature (ºC)', only_num)
    weather_df['Low temperature (ºC)'] = apply_in_column(weather_df, 'Low temperature (ºC)', only_num)
    weather_df['Probability of precipitation (%)'] = apply_in_column(weather_df, 'Probability of precipitation (%)', only_num)
    weather_df['Barometric pressure (mb)'] = apply_in_column(weather_df, 'Barometric pressure (mb)', only_num)
    return weather_df


def weather_info(weather_df):
    # Function to get the forecast info of the day: Forecast, High temperature, Low temperature and rain probability
    forecast = get_code(weather_df, weather_df.index[0], 'Forecast')
    high_temp = get_code(weather_df, weather_df.index[0], 'High temperature (ºC)')
    low_temp = get_code(weather_df, weather_df.index[0], 'Low temperature (ºC)')
    prob_precipitation = get_code(weather_df, weather_df.index[0], 'Probability of precipitation (%)')
    return forecast, high_temp, low_temp, prob_precipitation


def get_flights_df_m1(flight_list, flight_cols):  # Return a dataframe with the information of all flights requested
    flight_df_raw = get_df(flight_list)
    flight_df_raw1 = split_column(flight_df_raw, 3, '(', 'Departure city', 'Departure code')
    flight_df_raw2 = split_column(flight_df_raw1, 4, '(', 'Arrival city', 'Arrival code')
    flight_df_raw3 = strip_str_col(flight_df_raw2, 'Departure code', ')')
    flight_df_raw4 = strip_str_col(flight_df_raw3, 'Arrival code', ')')
    flight_df_clean = flight_df_raw4[[2, 'Departure city', 'Departure code', 'Arrival city', 'Arrival code',5, 6, 7, 8, 9, 11]]
    flights_df = flight_df_clean.columns(flight_cols)
    return flights_df


def get_flights_df_m2(flight_list, flight_cols2, flight_cols_final):  # Return a dataframe with the information of all flights requested
    flight_list_split = split_n(flight_list)
    flight_list_clean = remove_empties(flight_list_split)
    flight_df_raw = get_df(flight_list_clean, flight_cols2)
    flight_df_raw1 = split_column(flight_df_raw, 'Departure', '(', 'Departure city', 'Departure code')
    flight_df_raw2 = split_column(flight_df_raw1, 'Arrival', '(', 'Arrival city', 'Arrival code')
    flight_df_raw3 = strip_str_col(flight_df_raw2, 'Departure code', ')')
    flight_df_raw4 = strip_str_col(flight_df_raw3, 'Arrival code', ')')
    flights_df = flight_df_raw4[flight_cols_final]
    return flights_df


def currency_info(currency_table_route, departure_country, arrival_country):  # Returns currency info
    currency_df = get_df_from_csv(currency_table_route)
    departure_curr_df = get_row(currency_df, 'ENTITY', departure_country)
    departure_curr_code = get_value(departure_curr_df, 'Alphabetic Code')
    arrival_curr_df = get_row(currency_df, 'ENTITY', arrival_country)
    arrival_curr_code = get_value(arrival_curr_df, 'Alphabetic Code')
    arrival_curr_name = get_value(arrival_curr_df, 'Currency')
    return departure_curr_code, arrival_curr_code, arrival_curr_name


def hour_diff_calculate(arrival_h,departure_h):
    departure_hour = transform_hour(departure_h)
    arrival_hour = transform_hour(arrival_h)
    difference = departure_hour - arrival_hour
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











