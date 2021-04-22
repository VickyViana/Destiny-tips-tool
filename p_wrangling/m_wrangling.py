# IMPORTS

import pandas as pd
import re

# FUNCTIONS


def get_code(table_df, row, column):
    code_data = table_df.loc[row, column]
    return code_data


def get_city_df(table_df, column, data_code):
    city_df = table_df.loc[table_df[column] == data_code]
    return city_df


def get_destiny(flight_df, airports_df):  # Returns the variables city_name and country_name from the flight info
    city_code = get_code(flight_df,'iataCode','arrival')
    city_df = get_city_df(airports_df, 'iata_code', city_code)
    city_name = get_code(city_df, city_df.index[0], 'municipality')
    country_name = get_code(city_df, city_df.index[0], 'country_name')
    destiny = f'You are travelling to {city_name}, in {country_name}'
    return destiny, city_name, country_name


def not_day(text):  # Return a string deleting the last word
    short_text = ' '.join(text.split(' ')[:-1])
    return short_text


def only_num(text):  # Return ony the numbers in a string
    result = (re.findall('\d+', text))
    return ''.join(result)

def apply_in_column(table_df, column, fun_to_apply):  # Apply a function to a dataframe column
    table_df[column] = table_df[column].apply(fun_to_apply)
    return table_df[column]

def clean_weather(weather_df):  # To clean weather_df columns, to have more useful values
    weather_df['Forecast'] = apply_in_column(weather_df, 'Forecast', not_day)
    weather_df['High temperature (ºC)'] = apply_in_column(weather_df, 'High temperature (ºC)', only_num)
    weather_df['Low temperature (ºC)'] = apply_in_column(weather_df, 'Low temperature (ºC)', only_num)
    weather_df['Probability of precipitation (%)'] = apply_in_column(weather_df, 'Probability of precipitation (%)', only_num)
    weather_df['Barometric pressure (mb)'] = apply_in_column(weather_df, 'Barometric pressure (mb)', only_num)
    return weather_df

def weather_info(weather_df):
    forecast = get_code(weather_df, weather_df.index[0], 'Forecast')
    hight_temp = get_code(weather_df, weather_df.index[0], 'High temperature (ºC)')
    low_temp = get_code(weather_df, weather_df.index[0], 'Low temperature (ºC)')
    prob_precipitation = get_code(weather_df, weather_df.index[0], 'Probability of precipitation (%)')
    return forecast, hight_temp, low_temp, prob_precipitation

