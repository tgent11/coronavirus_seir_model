"""
This class contains the data for the country/state.
Data such as population and actual reported data for the Virus
Deaths, number of cases, etc.
"""
import os
import datetime
import fetch_data
USA = 'United States'

class CountryData(object):
    states_virus_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
    us_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    counties_url ='https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
    states_population_url = 'https://raw.githubusercontent.com/jakevdp/data-USstates/master/state-population.csv'
    # Use a local copy just in case github is down
    local_states = r'C:\Users\ngent\Documents\Coronavirus_Modeling\Data\covid-19-data\us-states.csv'
    local_usa = r'C:\Users\ngent\Documents\Coronavirus_Modeling\Data\covid-19-data\us.csv'
    CSV_HEADER = ['name', 'date', 'cases', 'deaths']

    def __init__(self, name='United States', county=False, update_data=False):
        self.name = name
        self.county = county
        self.update_data = update_data
        self.deaths = []
        self.cases = []
        self.dates = []
        self.csv_data = []
        # Corona virus data
        self.get_reported_data()
        # Population
        self.population = self.get_population_data()

    def get_reported_data(self):
        """
        Get the recorded corona virus data from either a local copy or github.
        Store the data in the appropriate class variables
        """
        # USA Country Data
        if self.name == USA:
            if os.path.exists(self.local_usa) and not self.update_data:
                data = fetch_data.fetch_us_data(self.local_usa)

            else:
                # Fetch corona virus data from github
                data = fetch_data.fetch_us_data(self.us_url)
            self.dates = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in list(data.date)]
            self.reported_cases = list(data.cases)
            self.deaths = list(data.deaths)

        # States
        elif not self.county:
            if os.path.exists(self.local_states) and not self.update_data:
                raw_data = fetch_data.fetch_us_data(self.local_states)

            else:
                raw_data = fetch_data.fetch_us_data(self.states_virus_url)
            # Remove unnecessary states, and set deaths, cases, etc
            self.fix_raw_state_data(raw_data)

        # Counties are weird, need special case to handle
        else:
            raw_data = fetch_data.fetch_us_data(self.counties_url)
            self.fix_raw_county_data(raw_data)

    def fix_raw_state_data(self, raw_data):
        """
        Parse the raw data, and remove states that don't match the "name"
        we're looking for. Add data to appropriate class variables.
        Create csv formatted data for writing output later
        :param raw_data: Full csv delimited data of all states
        :return:
        """
        ret_deaths = list(raw_data.deaths)
        ret_cases = list(raw_data.cases)
        ret_dates = list(raw_data.date)
        states = list(raw_data.state)

        self.csv_data.append(self.CSV_HEADER)
        # Start at end, remove unnecessary elements
        for i in range(len(list(raw_data.state)) - 1, -1, -1):
            if states[i] != self.name:
                del ret_deaths[i]
                del ret_cases[i]
                del ret_dates[i]
                del states[i]

            else:
                csv_row = []
                csv_row.append(self.name)
                csv_row.append(ret_dates[i])
                csv_row.append(ret_cases[i])
                csv_row.append(ret_deaths[i])

                # Insertion after header to account for backwards indexing of the for loop
                self.csv_data.insert(1, csv_row)
                ret_dates[i] = datetime.datetime.strptime(ret_dates[i], '%Y-%m-%d')

        self.deaths = ret_deaths
        self.reported_cases = ret_cases
        self.dates = ret_dates

    def fix_raw_county_data(self, raw_data):
        ret_deaths = list(raw_data.deaths)
        ret_cases = list(raw_data.cases)
        ret_dates = list(raw_data.date)
        states = list(raw_data.state)
        counties = list(raw_data.county)

        self.csv_data.append(self.CSV_HEADER)
        # Start at end, remove unnecessary elements
        for i in range(len(counties) - 1, -1, -1):
            if counties[i] != self.name:
                del ret_deaths[i]
                del ret_cases[i]
                del ret_dates[i]
                del states[i]
                del counties[i]

            else:
                csv_row = []
                csv_row.append(self.name)
                csv_row.append(ret_dates[i])
                csv_row.append(ret_cases[i])
                csv_row.append(ret_deaths[i])

                # Insertion after header to account for backwards indexing of the for loop
                self.csv_data.insert(1, csv_row)
                ret_dates[i] = datetime.datetime.strptime(ret_dates[i], '%Y-%m-%d')

        self.deaths = ret_deaths
        self.reported_cases = ret_cases
        self.dates = ret_dates

    def get_population_data(self):
        """
        Get the population for a given "name"
        i.e. self.name = 'United States', 'California' etc.
        :return: int of total population
        """
        return int(fetch_data.get_population(self.name))
