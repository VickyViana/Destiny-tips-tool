# **Destiny Tips Tool**
**Ironhack Madrid - Data Analytics Part Time - November 2020 - Final project**


This project is based on the creation of a tool that provides useful information about the destination of a flight. The aim of this application is to help unexpected travellers giving some helpful tips they would need in just one click. Once you introduce the flight code and the date, the data pipeline will collect the information required from different sources (datasets, APIs, web scraping...), and return some tips about the weather, currency and time zone difference of the specific arrival city. 

In this repository it will be explained how the tool has been built and how to run it.

<p align="center"><img src="https://s.abcnews.com/images/Lifestyle/GTY_airport_travel_jt_160612_16x9_992.jpg"></p>

## **Data sources** 

The sources where all the data have been taken are the following:

- **Flightradar24 web scrap**: in this web, when the flight code is introduced, we can get the city and country of arrival (https://www.flightradar24.com/data/flights)

- **World-airports-extended.csv dataset**: this dataset has been created from the merged of three primary datasets, in order to simplify the process. It is included in the "data" folder. The original datasets are:
	- world_airports.csv: downloaded from Ourairports (https://ourairports.com/data/)
	- airports-extended.csv: downloaded from Openfligts (https://openflights.org/data.html). Column "Tz database time zone" is taken from here.
	- country-codes.csv: downloaded from Datahub (https://datahub.io/core/country-codes). We extract columns "ISO4217-currency_alphabetic_code" and "ISO4217-currency_name" from here.

- **XE web scrap**: this web is a currency converter that works introducing the ISO code of the countries [Link](https://www.xe.com/es/currencyconverter/)

- **Prokerala web scrap**: This web displays the current hour in two countries according to the timezones inputted [Link](https://www.prokerala.com/travel/timezones/time-converter.php)

- **Weatherbit 16 Day Weather Forecast API**: this API provides all the information of the weather in the city requested. You can get an API key by free subscription. [Link](https://www.weatherbit.io/api/weather-forecast-16-day)
	


## **Tips provided** 

When the program is run with the values of flight code and date inputted, four types of information are shown:
- Destination: the city and country of arrival.
- Currency: the local currency and the actual exchange compared with the departure city.
- Time difference: the hours of difference between the departure and arrival cities.
- Weather forecast: information about different features of the weather in the arrival city, including temperature (media, maximum and minimum), clouds, rain, snow and humidity.



## **How it works** 

**Step One**: The input data (flight code and date) are introduced by web scraping in "Flightradar24", where the information of the specific flight is obtained. This information is stored in a dataframe called "flight". From here we will take the values of the departure airport code (departure_code) and the arrival airport code (arrival_code). In case there is a stopover flight, in the dataframe flight will be added a row with this flight data, and the arrival airport code will be taken from here.

**Step Two**: The airports codes previously obtained are searched in the word-airports-extended.csv dataset, extracting a dataframe for each airport (departure and arrival). In these dataframes are included useful values such as the arrival city and country names, the ISO country code, the time zone, the currency name and the currency ISO code.

**Step Three**: By selenium web scraping, the currency codes are inputted in XE web to obtain the rule of exchange between the currencies of each country.

**Step Four**: By selenium web scraping, the time zones of each city are entered in the web Pokerala, returning the actual hour for each. These hours are transformed into a suitable format (using datetime library) and subtracted to obtain time difference.

**Step Five**: For this step is used the API of Weatherbit, including in the url call the name of the arrival city and the country code. From here we obtain a dataframe with the information of 16 days from now, and we take the required data from the flight date line.

**Step Six**: Print the results obtained in previous steps, enclosing the data in different statements depending on their value.



## **Running methods**

The tool could be run by two methods:
- On console: running the file "main_script_2.py" and inputting the flight code and date as follows:

 $ python main_script_2.py -fc 'flight code' -d 'day number' -m 'month name' -y 'year number'
- With Streamlit: running the file "main_script.py" as follows:
$ streamlit run main_script.py

Then go to your local URL provided and you will see the tool interface, where you could input the flight data and see the resultant tips.



## **Technology stack**

- **Programming Language**: Python 3.8
- **Libraries in Use**: pandas 1.1.3, os, streamlit 0.80.0, datetime 4.3, queandl 3.6.0, regex 2020.10.15, requests 2.25.1, selenium 3.141.0



## **Folder structure**
```
└── Destiny-tips-tool
    ├── README.md
    ├── .gitignore
    ├── .env
    ├── requirements.txt
    ├── main_script.py
    ├── main_script_2.py
    ├── p_acquisition
    │   ├── __init__.py
    │   └── m_acquisition.py
    ├── p_wrangling
    │   ├── __init__.py
    │   └── m_wrangling.py
    ├── p_analysis
    │   ├── __init__.py
    │   └── m_analysis.py
    ├── notebooks
    │   ├── Jobs_Flight_&_Airports.ipynb
    │   ├── Jobs_Currency.ipynb
    │   ├── Jobs_Hour.ipynb
    │   └── Jobs_Weather.ipynb
    └── data
        ├── world-airports-extended.csv
        ├── world-airports.csv
        ├── airports-extended.csv
        └── country-codes_csv.csv
``` 

### **To Do**

Some improvements will be considered in the future:

- Improve the speed of running using parallelization of processes.
- Add the option of more than one stopover flight.
- Include results of other information that could be useful for the traveler, such as taxi companies in the arrival town or the official language of the city.

:airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: 


