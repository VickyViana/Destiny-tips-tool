# **Destiny-tips-tool**
Ironhack Madrid - Data Analytics Part Time - March 2021 - Final proyect


This proyect is based on the creation of a tool that provides useful information about the destination of a flight. Once you introduce the number of flight and the date, the pipline code will collect the information required from different sources (datasets, APIs, web scraping...), and return the specific 
The participation in the kaggle competition 'dapt202011mad - Predict diamond prices!' requires to create a machine learning model that could predict the price of diamonds depending on their properties. The model that gets the most accurate results will be the winner.

In this repository it will be explained how the model is designed step by step.

<p align="center"><img src="https://s.abcnews.com/images/Lifestyle/GTY_airport_travel_jt_160612_16x9_992.jpg"></p>

## **Data sources** 

- Flightradar24 web scrap: in this web, when the flight code is introduced, we can get the city and country of arrival (https://www.flightradar24.com/data/flights)

- world-airports-extended.csv dataset: this dataset has been created from the merged of three primary datasets, in order to simplify the process. It is included in "data" folder. The original datasets are:
	- world_airports.csv: downloaded from Ourairports (https://ourairports.com/data/)
	- airports-extended.csv: downloaded from Openfligts (https://openflights.org/data.html). Column "Tz database time zone" is taken from here.
	- country-codes.csv: downloaded from Datahub (https://datahub.io/core/country-codes). We extract columns "ISO4217-currency_alphabetic_code" and "ISO4217-currency_name" from here.

- XE web scrap: this web is a currency conversor that works introducing the ISO code of the countries [Link](https://www.xe.com/es/currencyconverter/)

- Prokerala web scrap: This web displays the current hour in two countries acording to the timezones inputed [Link](https://www.prokerala.com/travel/timezones/time-converter.php)

- Weatherbit 16 Day Weather Forecast API: this API provides all the information of the weather in the city requested. You can get an API key by free suscription. [Link](https://www.weatherbit.io/api/weather-forecast-16-day)
	


## **Tips provided** 

When the program is run with the values of flight code and date inputed, four types of information are shown:
- Destination: the city and country of arrival.
- Currency: the local currency and the actual exchange compared with departure city.
- Time difference: the hours of difference between the departure ande arrival cities.
- Weather forecast: information about different features of the weather in the arrival city, including temperature (media, maximum and minimum), clouds, rain, snow and humidity.



## **How it works** 

**First step**: The input data (flight code and date) are introduced by web scraping in "Flightradar24", where the information of the specific flight is obtainded. This information is stored in a dataframe called "flight". From here we will use the values of the arrival city (arrival_city), the departure airport code (departure_code) and the arrival airport code (arrival_code).
**Second step**: The airports codes previously obtained are searched in the word-airports-extended.csv dataset, extracting a dataframe for each airport (departure and arrival). In these dataframes are included useful values as the country, the time zone, the currency name and the currency ISO code.
**Third step**: The currrency codes are inputed in XE web to obtain the rule of 
- Columns 'cut', 'color' and 'clarity' are considered as categorical columns. Column 'price' will be the target of the model. A preprocessing transformer is applied to them implementing a SimpleImputer for the missing values (introducing the constant "missing") and encoding the strings to integers with OrdinalEncoder.

Both preprocessing transformers are join in one ColumnTransformer, called preprocessor.
The model is defined with a pipeline, using the previous explained preprocessor and a regressor, that in this case the chosen one has been LGBMRegressor, that seems to provide the best results.

After consider this transformation to the columns and define the prediction model, the dataset is split in train part and test part, and these parts are used to train the model. 

The following step is to check how good is the model. The first check is done with mean_squared_error, and the following results are obtained:
- test error: 551.94
- train error: 475.51
These are not bad results as both values are prety near to 0.

A second check with cross validation (from sklearn) is performed, considering as scoring 'neg_root_mean_squared_error' The mean of the scores obtained is 537.39, an acceptable score.


##**Running methods**

The tool could be run by two methods:
- On console: running the file "main_script_2.py" and inputting the flight code ande date as follows:

 $ python main_script_2.py -fc 'flight code' -d 'day number' -m 'month name' -y 'year number'
- With Streamlit: running the file "main_script.py" as follows:
$ streamlit run main_script.py

Then go to your local URL provided and you will see the tool interface, where you could input the flight data and see the resultant tips.




## **Technology stack**

- **Programming Language**: Python 3.8
- **Libraries in Use**: pandas 1.1.3, os, os.path, dotenv, argparse, streamlit 0.80.0, datetime 4.3, queandl 3.6.0, regex 2020.10.15, requests 2.25.1, selenium 3.141.0



## **Folder structure**
```
└── Destiny-tips-tool
    ├── .gitignore
    ├── README.md
    ├── main_script.py
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
    │   ├── Diamonds_kaggle_17.ipynb
    │   └── diamonds_prediction_17.csv
    └── data
        ├── world-airports-extended.csv
        ├── world-airports.csv
        ├── airports-extended.csv
        └── country-codes_csv.csv
``` 

:airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: :airplane: 


