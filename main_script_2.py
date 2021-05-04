# IMPORTS

import pandas as pd
import argparse
import os
from os.path import join, dirname
from dotenv import load_dotenv
from p_acquisition.m_acquisition import *
from p_wrangling.m_wrangling import *
from p_analysis.m_analysis import *


# CONSTANTS

flight_web = 'https://www.flightradar24.com/data/flights'
driver_route = '/home/viki/Bootcamp/drivers/chromedriver'
currency_web = 'https://www.xe.com/es/currencyconverter/'
path_airports = 'data/world-airports-extended.csv'
flight_cols = ['Date', 'Departure city', 'Departure code', 'Arrival city', 'Arrival code', 'Aircraft', 'Flight Time',
               'Scheduled Time Departure', 'Actual Time Departure', 'Scheduled Time Arrival', 'Status']
flight_cols2 = ['Aircraft', 'Date', 'Flight Time', 'Status', 'STD', 'Scheduled Time Departure', 'ATD',
              'Actual Time Departure', 'STA', 'Scheduled Time Arrival', 'FROM', 'Departure', 'To', 'Arrival']
hour_web = 'https://www.prokerala.com/travel/timezones/time-converter.php'


# FUNCTIONS


def argument_parser():
    # Parse arguments to this script
    parser = argparse.ArgumentParser(description='pass to the script the flight code you want to get results from')
    parser.add_argument("-fc", "--flight_code", help="flight code to get results from", type=str)
    parser.add_argument("-d", "--day", help="day of the flight", type=str)
    parser.add_argument("-m", "--month", help="month of the flight", type=str)
    parser.add_argument("-y", "--year", help="year of the flight", type=str)
    parser.add_argument("-fc2", "--flight_code2", help="connection flight", type=str)
    args = parser.parse_args()
    return args


def env_route(key):  # To get any key from dotenv
    dotenv_path = join(dirname("./.env"), '.env')
    load_dotenv(dotenv_path)
    weather_api_key = os.environ.get(key)
    return weather_api_key


def main(argument1, argument2, argument3, argument4, argument5):
    print('Getting info')
    weather_api_key = env_route('api_key')
    date_flight = date_short(argument2, argument3, argument4)
    flights_df = flight_connection_df(argument1, date_flight, argument5, driver_route, flight_web, flight_cols, flight_cols2)
    flight = flight_serie(flights_df, date_flight)
    departure_code, arrival_code = get_imp_flight_values(flight)
    airports_df = get_df_from_csv(path_airports)
    departure_airport_df, arrival_airport_df = get_airports_dfs(airports_df, departure_code, arrival_code)
    arrival_city, departure_country, arrival_country, arrival_country_tz, departure_country_tz, arrival_curr_code, \
           departure_curr_code, arrival_curr_name, departure_curr_name, arrival_country_code = \
        get_imp_airports_values(arrival_airport_df, departure_airport_df)

    # weather_df = get_weather_df(weather_web, arrival_country, airport_name, weather_cols)

    # flight_df = get_flight_info_df(aed_flight, argument1)

    rule = get_currency_change(driver_route, currency_web, departure_curr_code, arrival_curr_code)
    departure_h, arrival_h = get_tz_dif(driver_route, hour_web, departure_country_tz, arrival_country_tz)
    hour_diff = hour_diff_calculate(arrival_h, departure_h)
    weather_df = get_api_weather(arrival_city, arrival_country_code, weather_api_key)
    temp, max_temp, min_temp, rain, snow, humidity, clouds = weather_info(date_flight, weather_df)

    print(print_destiny(arrival_city, arrival_country))
    print(print_currency(departure_curr_code, arrival_curr_code, arrival_city, departure_country, arrival_country,
                         arrival_curr_name, rule))
    print(print_hour_diff(hour_diff))
    print(print_weather(temp, max_temp, min_temp, rain, snow, humidity, clouds))
    print(f'Happy trip!')


if __name__ == '__main__':

    main(argument_parser().flight_code, argument_parser().day, argument_parser().month, argument_parser().year, argument_parser().flight_code2)