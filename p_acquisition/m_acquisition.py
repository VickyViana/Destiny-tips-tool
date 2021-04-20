import pandas as pd
import quandl
from sqlalchemy import create_engine
import requests
from bs4 import BeautifulSoup

# Constants

airports_cols = ['Airport_ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude', 'Longitude', 'Altitude',
                 'Timezone', 'DST', 'Tz database timezone', 'Type', 'Source']

# Functions


def get_airports(path):  # Function to get airports dataset
    airports = pd.read_csv(path, header=None)
    return airports


def setup_quandl(api_key):  # Function to apply API key
    quandl.ApiConfig.api_key = api_key

