# IMPORTS

from p_wrangling.m_wrangling import *
from datetime import datetime
from datetime import timedelta

# FUNCTIONS


def add_1_day(date):  # To transform date in datetime format an add 1 day
    date_changed = datetime.strptime(date, "%d %b %Y")
    new_date = date_changed + timedelta(days=1)
    return new_date


def get_imp_flight_values(flight_info):  # Returns departure and arrival codes from flight df info
    try:
        departure_code = get_value(flight_info, 'Departure code')
    except:
        print('No data from your flight is available yet. Try again 7 days before flight departure day.')
        exit()
    else:
        if len(flight_info) == 1:
            arrival_code = get_value(flight_info, 'Arrival code')
        if len(flight_info) == 2:
            arrival_code = flight_info['Arrival code'].values[1]

    return departure_code, arrival_code


def get_imp_airports_values(arrival_airport_df, departure_airport_df):  # Returns all data needed from airports df
    arrival_city = get_value(arrival_airport_df, 'municipality')
    arrival_country = get_value(arrival_airport_df, 'country_name')
    departure_country = get_value(departure_airport_df, 'country_name')
    arrival_country_tz = get_value(arrival_airport_df, 'Tz database time zone')
    departure_country_tz = get_value(departure_airport_df, 'Tz database time zone')
    arrival_curr_code = get_value(arrival_airport_df, 'ISO4217-currency_alphabetic_code')
    departure_curr_code = get_value(departure_airport_df, 'ISO4217-currency_alphabetic_code')
    arrival_curr_name = get_value(arrival_airport_df, 'ISO4217-currency_name')
    departure_curr_name = get_value(departure_airport_df, 'ISO4217-currency_name')
    arrival_country_code = get_value(arrival_airport_df, 'iso_country')
    return arrival_city, departure_country, arrival_country, arrival_country_tz, departure_country_tz, arrival_curr_code, \
           departure_curr_code, arrival_curr_name, departure_curr_name, arrival_country_code


def flight_connection_df(flight1_code, date_flight, flight2_code, driver_route, flight_web, flight_cols, flight_cols2):
    #  Returns flight df with one or tw rows, depending if there are one or two flight codes
    flight1_df = get_flights_df(driver_route, flight_web, flight1_code, flight_cols, flight_cols2, date_flight)
    if flight2_code != None:
        flight2_df = get_flights_df(driver_route, flight_web, flight2_code, flight_cols, flight_cols2, date_flight)
        if len(flight2_df) == 0:
            date_tomorrow = add_1_day(date_flight)
            new_date = date_tomorrow.strftime("%d %b %Y")
            flight2_df = get_flights_df(driver_route, flight_web, flight1_code, flight_cols, flight_cols2, new_date)
        flight_df = flight1_df.append(flight2_df)
    else:
        flight_df = flight1_df

    return flight_df


def get_airports_dfs(airports_df, departure_code, arrival_code):  # Returns dfs for departure and arrival airports
    departure_airport_df = get_row(airports_df, 'iata_code', departure_code)
    arrival_airport_df = get_row(airports_df, 'iata_code', arrival_code)
    return departure_airport_df, arrival_airport_df


def print_destiny(city_name, country_name):  # Print destination tip
    destiny = f'You are travelling to {city_name}, in {country_name}.'
    return destiny


def calculate_day(date):
    today = datetime.now()
    flight_day = datetime.strptime(date, '%d %b %Y')
    day_row = flight_day - today
    return day_row


def get_weather_day(weather_df, day_row):
    weather_day_df = weather_df.iloc[day_row]
    return weather_day_df


def print_currency(departure_curr_code, arrival_curr_code, arrival_city, departure_country, arrival_country, arrival_curr_name, rule):
    # Print currency tip
    if len(arrival_curr_code) != 3:
        error_message = 'No currency data available for the arrival country'
        return error_message
    if departure_curr_code == arrival_curr_code:
        if departure_country == arrival_country:
            curr_solution1 = f"{arrival_city} is also in {departure_country}, thus the {arrival_curr_name} is used. You won't need to change!"
            return curr_solution1
        else:
            curr_solution2 = f'In {departure_country} and {arrival_country} is used the same currency, the {arrival_curr_name}.'
            return curr_solution2
    else:
        curr_solution3 = f"The currency in {arrival_country} is the {arrival_curr_name}. Don't forget that {rule}."
        return curr_solution3


def print_hour_diff(hour_diff):  # Print hour tip
    if hour_diff == 'No':
        return 'There is no time data available for your trip.'
    elif hour_diff == 0:
        return 'There is no time difference.'
    elif hour_diff < 0:
        return f'There is a time difference of {hour_diff} hours. You have to set the clock back.'
    else:
        return f'There is a time difference of +{hour_diff} hours. You have to set the clock forward.'


def print_weather(temp, max_temp, min_temp, rain, snow, humidity, clouds):  # Print weather tip
    temperatures = f'There will be an average temperature of {temp} ºC, with {max_temp} ºC of maximum and {min_temp} ºC of minimum.'
    humid = f'There will be a humidity of {humidity}%.'
    if clouds < 20:
        clouding = f'It will be a cloudless day.'
    elif clouds > 20 & clouds < 70:
        clouding = f'It will be partly cloudy.'
    elif clouds >= 70:
        clouding = f'It will be very cloudy.'
    if rain == 0:
        raining = f"It won't rain."
    elif rain >0 & rain <= 60:
        raining = f"There is a {rain}% probability of rain."
    elif rain > 60:
        raining = f"There is a {rain}% probability of rain. Don't forget your umbrella."
    if snow != 0:
        snowing = f'It will snow.'
    else:
        snowing = ''
    return f'{temperatures} {clouding} {raining} {snowing} {humid}'

