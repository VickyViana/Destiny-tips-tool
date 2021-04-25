# IMPORTS

import pandas as pd
import argparse
from p_acquisition.m_acquisition import *
from p_wrangling.m_wrangling import *
from p_analysis.m_analysis import *

# CONSTANTS

flight_web = 'https://www.flightradar24.com/data/flights'
aed_flight = 'http://aviation-edge.com/v2/public/flights?key=25034e-9edde7&flightIata='
forecast_web ='https://www.weatherwx.com/forecast.php?config=&forecast=pass&pass=tafINT'
driver_route = '/home/viki/Bootcamp/drivers/chromedriver'
weather_web = 'https://www.weatherwx.com/forecast.php?config=&forecast=pass&pass=tafINT'
path_airports = 'data/world-airports.csv'
flight_cols = ['Date', 'Departure city', 'Departure code', 'Arrival city', 'Arrival code', 'Aircraft', 'Flight Time',
               'Scheduled Time Departure', 'Actual Time Departure', 'Scheduled Time Arrival', 'Status']
weather_cols = ['Forecast', 'High temperature (ºC)', 'Low temperature (ºC)',
            'Probability of precipitation (%)', 'Wind', 'Barometric pressure (mb)']
flight_cols2 = ['Aircraft', 'Date', 'Flight Time', 'Status', 'STD', 'Scheduled Time Departure', 'ATD',
              'Actual Time Departure', 'STA', 'Scheduled Time Arrival', 'FROM', 'Departure', 'To', 'Arrival']

# FUNCTIONS


def argument_parser():
    # Parse arguments to this script
    parser = argparse.ArgumentParser(description='pass to the script the flight code you want to get results from')
    parser.add_argument("-fc", "--flight_code", help="flight code to get results from", type=str)
    parser.add_argument("-d", "--day", help="day of the flight", type=str)
    parser.add_argument("-m", "--month", help="month of the flight", type=str)
    parser.add_argument("-y", "--year", help="year of the flight", type=str)
    args = parser.parse_args()
    return args


def flight_mode_selector(flight_list, flight_cols, flight_cols2):
    if flight_list[0] == "":
        flight_df = get_flights_df_m1(flight_list, flight_cols2)
    else:
        flight_df = get_flights_df_m2(flight_list, flight_cols2, flight_cols)
    return flight_df


def main(argument1, argument2, argument3, argument4):
    print('Getting info')
    date = date_short(argument2, argument3, argument4)
    flight_list = get_flight_info(driver_route, flight_web, argument1)
    flights_df = flight_mode_selector(flight_list, flight_cols, flight_cols2)
    flight = flight_serie(flights_df, date)
    arrival_city, departure_code, arrival_code = get_imp_flight_values(flight)
    airports_df = get_df_from_csv(path_airports)
    departure_airport_df, arrival_airport_df = get_airports_dfs(airports_df, departure_code, arrival_code)
    arrival_country = get_imp_airports_values(arrival_airport_df)
    weather_df = get_weather_df(weather_web, arrival_country, airport_name, weather_cols)

    # flight_df = get_flight_info_df(aed_flight, argument1)


    # city_name, country_name = get_destiny(flight_df, airports_df)
    #

    print(print_destiny(arrival_city, arrival_country))
    #print(print_weather)


if __name__ == '__main__':
    main(argument_parser().flight_code, argument_parser().day, argument_parser().month, argument_parser().year)