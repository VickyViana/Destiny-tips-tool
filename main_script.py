# IMPORTS

import pandas as pd
import argparse
from p_acquisition.m_acquisition import *
from p_wrangling.m_wrangling import *
from p_analysis.m_analysis import *

# CONSTANTS

aed_flight = 'http://aviation-edge.com/v2/public/flights?key=25034e-9edde7&flightIata='
forecast_web ='https://www.weatherwx.com/forecast.php?config=&forecast=pass&pass=tafINT'
driver_route = '/home/viki/Bootcamp/drivers/chromedriver'
weather_web = 'https://www.weatherwx.com/forecast.php?config=&forecast=pass&pass=tafINT'
path_airports = 'data/world-airports.csv'
weather_cols = ['Forecast', 'High temperature (ºC)', 'Low temperature (ºC)',
            'Probability of precipitation (%)', 'Wind', 'Barometric pressure (mb)']

# FUNCTIONS


def argument_parser():
    # Parse arguments to this script
    parser = argparse.ArgumentParser(description='pass to the script the flight code you want to get results from')
    parser.add_argument("-fc", "--flight_code", help="flight code to get results from", type=str)
    parser.add_argument("-da", "--date", help="date of the flight", type=int)
    args = parser.parse_args()
    return args


def main(argument1, argument2):
    print('Getting info')
    flight_df = get_api_info_df(aed_flight, argument1)
    airports_df = get_df_from_csv(path_airports)
    # departure_code = get_code(flight_df, 'iataCode','departure')
    # arrival_code = get_code(flight_df,'iataCode','arrival')
    destiny, city_name, country_name = get_destiny(flight_df, airports_df)
    weather_df = get_weather(weather_web, country_name, airport_name, weather_cols)

    print(destiny)



if __name__ == '__main__':
    main(argument_parser().flight_code, argument_parser().date)