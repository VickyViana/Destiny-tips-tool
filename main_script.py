# IMPORTS
import argparse
from p_acquisition.m_acquisition import *
from p_wrangling.m_wrangling import *
from p_analysis.m_analysis import *


def main():
    airports = get_airports('./data/airports-extended.csv')
    airports.columns = airports_cols
    print(airports)
    print(airports['Timezone'].unique())


if __name__ == '__main__':
    main()
