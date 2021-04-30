# IMPORTS
from p_acquisition.m_acquisition import *
from p_wrangling.m_wrangling import *
from datetime import datetime

# FUNCTIONS


def flight_serie(flight_df, date):
    flight_info = get_row(flight_df, 'Date', date)
    return flight_info


def get_imp_flight_values(flight_info):
    arrival_city = get_value(flight_info, 'Arrival city')
    departure_code = get_value(flight_info, 'Departure code')
    arrival_code = get_value(flight_info, 'Arrival code')
    return arrival_city, departure_code, arrival_code


def get_imp_airports_values(arrival_airport_df, departure_airport_df):
    arrival_country = get_value(arrival_airport_df, 'country_name')
    departure_country = get_value(departure_airport_df, 'country_name')
    arrival_country_tz = get_value(arrival_airport_df, 'Tz database time zone')
    departure_country_tz = get_value(departure_airport_df, 'Tz database time zone')
    arrival_curr_code = get_value(arrival_airport_df, 'ISO4217-currency_alphabetic_code')
    departure_curr_code = get_value(departure_airport_df, 'ISO4217-currency_alphabetic_code')
    arrival_curr_name = get_value(arrival_airport_df, 'ISO4217-currency_name')
    departure_curr_name = get_value(departure_airport_df, 'ISO4217-currency_name')
    return departure_country, arrival_country, arrival_country_tz, departure_country_tz, arrival_curr_code, \
           departure_curr_code, arrival_curr_name, departure_curr_name


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


def print_currency(departure_curr_code, arrival_curr_code, arrival_city, departure_country, arrival_country, arrival_curr_name, rule):
    if departure_curr_code == arrival_curr_code:
        if departure_country == arrival_country:
            curr_solution1 = f"{arrival_city} is also in {departure_country}, thus the {arrival_curr_name} is used. You won't need to change!"
            return curr_solution1
        else:
            curr_solution2 = f'In {departure_country} and {arrival_country} is used the same currency, the {arrival_curr_name}'
            return curr_solution2
    else:
        curr_solution3 = f"The currency in {arrival_country} is {arrival_curr_name}. Don't forget that {rule}"
        return curr_solution3


def print_hour_diff(hour_diff):
    if hour_diff == 0:
        return 'There are no time difference'
    else:
        return f'There is a time difference of {hour_diff} hours'



