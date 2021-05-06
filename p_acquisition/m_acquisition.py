# IMPORTS

import pandas as pd
import quandl
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# Constants

airports_cols = ['Airport_ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude', 'Longitude', 'Altitude',
                 'Timezone', 'DST', 'Tz database timezone', 'Type', 'Source']

# Functions


def get_df_from_csv(path):  # Function to get airports dataset
    table_df = pd.read_csv(path)
    return table_df


def setup_quandl(api_key):  # Function to apply API key
    quandl.ApiConfig.api_key = api_key


def get_driver(route):  # Function to get selenium driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(route, options=chrome_options)
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


def click_button_xpath(driver, xpath):  # To click a selected button
    button = driver.find_element_by_xpath(xpath)
    clicker = driver.execute_script("arguments[0].click();", button)
    return clicker


def fill_box(driver, text):  # Fill a text box with the text provided
    filler = driver.send_keys(text)
    return filler


def click_enter(driver):  # Click the key Enter when needed
    click = driver.send_keys(Keys.ENTER)
    return click


def get_flight_info(route, web, flight_code):
    # Returns a df taken from the web with all the flights availables with the flight code entered
    driver = get_driver(route)
    get_web(driver, web)
    click_button(driver, "btn.btn-blue")
    flight_box = find_by_id(driver, 'searchFlight')
    fill_box(flight_box, flight_code)
    WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, "tt-dataset-aircraftList")))
    flight_selection = find_by_class(driver, 'tt-dataset-aircraftList')
    flight_selection.click()
    try:
        WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'tbody')))
    except:
        print("The flight code does not exist, please try again.")
        exit()
    else:
        table_f = driver.find_element_by_css_selector('tbody')

    rows = table_f.find_elements_by_class_name('data-row')
    flight_raw = []
    for row in rows:
        cells = row.find_elements_by_tag_name('td')
        for cell in cells:
            flight_raw.append(str(cell.text))
    return flight_raw


def get_airports_info(path_airports):  # Read the airports dataframe
    airports_df = get_df_from_csv(path_airports)
    return airports_df


def get_currency_change(route, web, departure_curr_code, arrival_curr_code):  # Returns currency info
    driver = get_driver(route)
    get_web(driver, web)
    click_button_xpath(driver, "//button[@class='button__BaseButton-sc-1qpsalo-0 ctapkr']")
    WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.ID, "midmarketFromCurrency")))
    first_box = find_by_id(driver, 'midmarketFromCurrency')
    fill_box(first_box, departure_curr_code)
    click_enter(first_box)
    second_box = find_by_id(driver, 'midmarketToCurrency')
    fill_box(second_box, arrival_curr_code)
    click_enter(second_box)
    click_button_xpath(driver, "//button[@type='submit']")
    WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, "unit-rates___StyledDiv-sc-1dk593y-0.dEqdnx")))
    rule = find_by_class(driver, "unit-rates___StyledDiv-sc-1dk593y-0.dEqdnx")
    return rule.text


def get_tz_dif(route, web, departure_timezone, arrival_timezone):  # Returns city hours from time zones web
    driver = get_driver(route)
    get_web(driver, web)
    departure_box = find_by_id(driver, 'loc1')
    departure_box.clear()
    fill_box(departure_box, departure_timezone)
    arrival_box = find_by_id(driver, 'loc2')
    fill_box(arrival_box, arrival_timezone)
    click_enter(arrival_box)
    departure_hour = find_by_id(driver, 'time1')
    departure_h = departure_hour.get_attribute('value')
    arrival_hour = find_by_id(driver, 'time2')
    arrival_h = arrival_hour.get_attribute('value')
    return departure_h, arrival_h


def get_api_weather(arrival_city, arrival_country_code, api_weather_key):
    # Returns df with 16 days forecast from weather web
    url = f'https://api.weatherbit.io/v2.0/forecast/daily?city={arrival_city}&country={arrival_country_code}&key={api_weather_key}'
    html_weather = requests.get(url).json()
    html_dic = html_weather['data']
    weather_df = pd.DataFrame(html_dic)
    return weather_df
