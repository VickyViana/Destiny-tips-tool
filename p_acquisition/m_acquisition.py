# IMPORTS

import pandas as pd
import quandl
import re
from sqlalchemy import create_engine
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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


def find_by_class(driver, element_class):  # Find an element in html code by class name
    element = driver.find_element_by_class_name(element_class)
    return element


def find_by_tag(table, tag):  # Find an element in html code by tag name
    element = table.find_elements_by_tag_name(tag)
    return element


def find_by_id(driver, id_data):  # Find an element in html code by id
    element = driver.find_element_by_id(id_data)
    return element


def click_button(driver, element_class):  # To click a selected button
    button = find_by_class(driver, element_class)
    clicker = driver.execute_script("arguments[0].click();", button)
    return clicker


def select_dropdown(driver, name_menu, name_search):  # To select an option in a drop-down menu
    selection = driver.find_element_by_xpath("//select[@name=name_menu]/option[text()=name_search]").click()
    return selection


def fill_box(driver, text):
    filler = driver.send_keys(text)
    return filler

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


def get_flight_info(route, web, flight_code):
    driver = get_driver(route)
    get_web(driver, web)
    click_button(driver, "btn.btn-blue")
    flight_box = find_by_id(driver, 'searchFlight')
    fill_box(flight_box, flight_code)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "tt-dataset-aircraftList")))
    flight_selection = find_by_class(driver, 'tt-dataset-aircraftList')
    flight_selection.click()
    table = driver.find_element_by_css_selector('tbody')
    rows = table.find_elements_by_class_name('data-row')
    flight_raw = []
    for row in rows:
        cells = row.find_elements_by_tag_name('td')
        for cell in cells:
            flight_raw.append(str(cell.text))
    return flight_raw


def get_airports_info(path_airports):
    airports_df = get_df_from_csv(path_airports)
    return airports_df


def get_weather_df(route, web, country_name, airport_name, weather_cols):  # Can get weather information from an airport
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
