# IMPORTS

import pandas as pd
import quandl
import re
from sqlalchemy import create_engine
import requests
from selenium import webdriver


# Constants

airports_cols = ['Airport_ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude', 'Longitude', 'Altitude',
                 'Timezone', 'DST', 'Tz database timezone', 'Type', 'Source']
aed_flight = 'http://aviation-edge.com/v2/public/flights?key=25034e-9edde7&flightIata='

# Functions


def get_api_info_df(route,flight):  # Function to get flight information from API
    url = (f'{route}{flight}')
    html_flight = requests.get(url).json()
    html_dic = html_flight[0]
    api_df = pd.DataFrame.from_dict(html_dic)
    return api_df


def get_df_from_csv(path):  # Function to get airports dataset
    table_df = pd.read_csv(path)
    return table_df


def setup_quandl(api_key):  # Function to apply API key
    quandl.ApiConfig.api_key = api_key


def get_driver(route):  # Function to get selenium driver
    driver = webdriver.Chrome(route)
    return driver


def get_web(driver, web):  # To open requested web in driver browser
    web_activation = driver.get(web)
    return web_activation


def find_by_class(driver, element_class):
    element = driver.find_element_by_class_name(element_class)
    return element


def find_by_tag(table, tag):
    element = table.find_elements_by_tag_name(tag)
    return element


def click_button(driver, element_class):  # To click a selected button
    button = find_by_class(driver, element_class)
    clicker = driver.execute_script("arguments[0].click();", button)
    return clicker


def select_dropdown(driver, name_menu, name_search):  # To select an option in a drop-down menu
    selection = driver.find_element_by_xpath("//select[@name=name_menu]/option[text()=name_search]").click()
    return selection


'''
Function to order the data as we need and fill the empty data with 0. 
This will help when the data will be introduce in a dataset 
The data will be ordered as follows:
1 - Forecast
2 - High temperature
3 - Low temperature
4 - Probability of precipitation
5 - Wind
6 - Barometric pressure
'''


def reorder_func(day_weather_list):
    reordered_weather = [day_weather_list[0], day_weather_list[1], day_weather_list[2]]
    for i in range(2, len(day_weather_list)):
        if 'precipitation' in day_weather_list[i]:
            reordered_weather.append(day_weather_list[i])
    if len(reordered_weather)< 4:
        reordered_weather.append('0')

    for i in range(2, len(day_weather_list)):
        if 'wind' in day_weather_list[i]:
            reordered_weather.append(day_weather_list[i])
    if len(reordered_weather)< 5:
        reordered_weather.append('0')

    for i in range(2, len(day_weather_list)):
        if 'pressure' in day_weather_list[i]:
            reordered_weather.append(day_weather_list[i])
    if len(reordered_weather)< 6:
        reordered_weather.append('0')

    return reordered_weather


def get_weather(web, country_name, airport_name, weather_cols):  # Can get weather information from an airport
    driver = get_driver(route)
    get_web(driver, web)
    click_button(driver, "btn.btn-primary.btn-sm.acceptcookies")
    select_dropdown(driver, 'Country', country_name)
    select_dropdown(driver, 'Places', airport_name)
    click_button(driver, "btn.btn-default.btn-sm")
    table = driver.find_element_by_class_name('panel.panel-primary.article')
    rows = table.find_elements_by_tag_name('table')
    weather_raw = []
    for row in rows:
        cells = row.find_elements_by_tag_name('td')
        weather_raw.append(cells[1].text)
    weather_raw_list = [[x] for x in weather_raw]
    weather_raw_divided = [re.split('[,.]', y) for x in weather_raw_list for y in x]
    ordered_weather = []
    for x in weather_raw_divided:
        sublist = reorder_func(x)
        ordered_weather.append(sublist)
    weather_df = pd.DataFrame(ordered_weather, columns=weather_cols)
    return weather_df





