# IMPORTS
from p_acquisition.m_acquisition import *
from p_wrangling.m_wrangling import *
from datetime import datetime

# FUNCTIONS


def get_value(data_serie, column):
    code = data_serie[column].values[0]
    return code


def flight_serie(flight_df, date):
    flight_info = get_row(flight_df, 'Date', date)
    return flight_info


def get_imp_flight_values(flight_info):
    arrival_city = get_value(flight_info, 'Arrival city')
    departure_code = get_value(flight_info, 'Departure code')
    arrival_code = get_value(flight_info, 'Arrival code')
    return arrival_city, departure_code, arrival_code


def get_imp_airports_values(arrival_airport_df):
    arrival_country = get_value(arrival_airport_df, 'country_name')
    return arrival_country


def get_airports_dfs(airports_df, departure_code, arrival_code):
    departure_airport_df = get_row(airports_df, 'iata_code', departure_code)
    arrival_airport_df = get_row(airports_df, 'iata_code', arrival_code)
    return departure_airport_df, arrival_airport_df


def print_destiny(city_name, country_name):
    destiny = f'You are travelling to {city_name}, in {country_name}'
    return destiny


def calculate_day(date):
    today = datetime.now()
    flight_day = datetime.strptime(date, '%d %b %Y')
    day_row = flight_day - today
    return day_row


def get_weather_day(weather_df, day_row):
    weather_day_df = weather_df.iloc[day_row]
    return weather_day_df


def print_weather(forecast, high_temp, low_temp, prob_precipitation):
    weather_tip = f'It will be {forecast}, with {high_temp} ºC of highest temperature, and {low_temp} ºC of lowest temperature'
    if prob_precipitation != 0:
        rain_tip = f"There will be {prob_precipitation}% probability of rain, so don't forget your umbrella!"
    return weather_tip, rain_tip


