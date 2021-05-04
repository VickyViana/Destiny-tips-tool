# IMPORTS

import streamlit as st
import pandas as pd
import argparse
import os
from os.path import join, dirname
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from p_acquisition.m_acquisition import *
from p_wrangling.m_wrangling import *
from p_analysis.m_analysis import *

# CONSTANTS

flight_web = 'https://www.flightradar24.com/data/flights'
forecast_web ='https://www.weatherwx.com/forecast.php?config=&forecast=pass&pass=tafINT'
driver_route = '/home/viki/Bootcamp/drivers/chromedriver'
currency_web = 'https://www.xe.com/es/currencyconverter/'
path_airports = 'data/world-airports-extended.csv'
flight_cols = ['Date', 'Departure city', 'Departure code', 'Arrival city', 'Arrival code', 'Aircraft', 'Flight Time',
               'Scheduled Time Departure', 'Actual Time Departure', 'Scheduled Time Arrival', 'Status']
flight_cols2 = ['Aircraft', 'Date', 'Flight Time', 'Status', 'STD', 'Scheduled Time Departure', 'ATD',
              'Actual Time Departure', 'STA', 'Scheduled Time Arrival', 'FROM', 'Departure', 'To', 'Arrival']
hour_web = 'https://www.prokerala.com/travel/timezones/time-converter.php'


# FUNCTIONS

def env_route(key):  # To get any key from dotenv
    dotenv_path = join(dirname("./.env"), '.env')
    load_dotenv(dotenv_path)
    weather_api_key = os.environ.get(key)
    return weather_api_key


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
    # Selection of the transformation needed to flight_list
    if flight_list[0] == "":
        flight_df = get_flights_df_m1(flight_list, flight_cols2)
    else:
        flight_df = get_flights_df_m2(flight_list, flight_cols2, flight_cols)
    return flight_df


def main_run(argument1, argument2, argument3, argument4):
    print('Getting info')
    #destiny_tip = 'Here you will see your destination city and country'
    #currency_change = 'Here you will see the currency change comparing with the departure currency'
    #hour_difference = 'Here you will see the hour difference between departure and arrival city'
    #weather_tips = 'Here you will see the weather forecast of the destination city'
    weather_api_key = env_route('api_key')
    date_flight = date_short(argument2, argument3, argument4)
    flight_list = get_flight_info(driver_route, flight_web, argument1)
    flights_df = flight_mode_selector(flight_list, flight_cols, flight_cols2)
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

    destiny_tip = print_destiny(arrival_city, arrival_country)
    currency_change = print_currency(departure_curr_code, arrival_curr_code, arrival_city, departure_country, arrival_country,
                         arrival_curr_name, rule)
    hour_difference = print_hour_diff(hour_diff)
    weather_tips = print_weather(temp, max_temp, min_temp, rain, snow, humidity, clouds)
    return destiny_tip, currency_change, hour_difference, weather_tips


def main():
    header = st.beta_container()
    comments = st.beta_container()
    input_flight = st.beta_container()
    input_date = st.beta_container()
    input_submit = st.beta_container()
    destiny = st.beta_container()
    currency = st.beta_container()
    hour_change = st.beta_container()
    weather = st.beta_container()

    with header:
        st.title('Destiny Tips')
        st.subheader("This tool will help you to get the useful information of your upcoming flight")

    with comments:
        st.text("Don't forget this tool works only for direct flights that departs before 7 days")

    with input_flight:
        #first_col, second_col, third_col = st.beta_columns(3)
        flight_code = st.text_input('Enter your flight code', 'Flight code')

    with input_date:
        first_col, second_col, third_col = st.beta_columns(3)
        day = first_col.selectbox('Day', options=['01', '02', '03', '04', '05', '06', '07', '08',
                            '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23',
                                                                      '24', '25', '26', '27', '28', '29', '30', '31'])
        month = second_col.selectbox('Month', options=['January', 'February', 'March', 'April', 'May', 'June', 'July',
                                                         'August', 'September', 'October', 'November', 'December'])
        year = third_col.selectbox('Year', options=['2021', '2022', '2023'])

    with input_submit:
        submit = second_col.button('Get your trip tips')
        if submit:
            gif_runner = st.image('https://media.giphy.com/media/lmin3DgycfcRqHQmQF/giphy.gif')
            destiny_tip, currency_change, hour_difference, weather_tips = main_run(flight_code, day, month, year)
            gif_runner.empty()

    with destiny:
        st.header("Destiny tip")
        if submit:
            st.write(destiny_tip)


    with currency:
        st.header("Money exchange tip")
        if submit:
            st.write(currency_change)

    with hour_change:
        st.header("Time difference tip")
        if submit:
            st.write(hour_difference)

    with weather:
        st.header("Weather tip")
        if submit:
            st.write(weather_tips)


if __name__ == '__main__':
    main()
