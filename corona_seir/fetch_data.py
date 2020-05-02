import urllib.request
import pandas
import data_utilities
import csv

class CSVFileReadError(IOError):
    pass


def fetch_us_data(file):
    """
    Try to read csv data from file. Return pandas object
    file can be local path, or github address
    :param file:
    :return:
    """
    try:
        return pandas.read_csv(file, error_bad_lines=False)
    except:
        print("Can't load csv file, either github or local copy")


def get_population(name, file='nst-est2019-popchg2010_2019.csv', key='POPESTIMATE2019'):
    """
    Get population for USA, or a state based on 'name'.
    Default file param should be saved in same working folder as code.
    :param name:
    :param file:
    :param key:
    :return:
    """
    # CSV File Format: SUMLEV	REGION	DIVISION	STATE	NAME    POPESTIMATE2018 POPESTIMATE2019
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['NAME'] == name:
                return row[key]
    return 0
