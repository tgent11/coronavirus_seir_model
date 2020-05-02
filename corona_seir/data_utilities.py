
CACHETIMESECONDS = 3600 * 3  # be nice to the API to not get banned

APIURL = 'https://coronavirus-tracker-api.herokuapp.com/all'
FILENAME = 'covid-19_data.json'

import datetime
import numpy as np
import scipy.ndimage.interpolation  # shift function
import csv


def delay(npArray, days):
    """shift to right, fill with 0, values fall off!"""
    return scipy.ndimage.interpolation.shift(npArray, days, cval=0)


def get_offset_x(deaths, D_model, data_offset='auto'):
    """
    Leftover code, don't know wtf is going on here :)
    All it does is best match the data and shift the days to best align with actual cases
    :param deaths:
    :param D_model:
    :param data_offset:
    :return:
    """
    x_days = list(range(len(deaths)))
    X_days = np.array(x_days) - min(x_days)
    if data_offset == 'auto':
        D_data = deaths

        # log to emphasize lower values (relative error)   http://wrogn.com/curve-fitting-with-minimized-relative-error/
        D_data = np.log(np.array(D_data, dtype='float64') + 1)
        D_model = np.log(D_model + 1)

        mini = 9e9
        miniO = None
        for o in range(0,150):  # todo: dat number...
            oDd = np.pad(D_data, (o, 0))  # different than delay/shift, extends length
            oDm = D_model[:len(D_data) + o]
            rms = np.sqrt(np.mean(np.square((oDd - oDm))/(1 + oDm)))  # hacky but seems to do the job
            if rms < mini:
                mini = rms
                miniO = o
        print("date offset:", miniO)
        data_offset = miniO
    return data_offset


def model_to_world_time(num_days_to_shift, dates):
    """
    Convert to dates that are readable
    :param num_days_to_shift:
    :param dates:
    :return:
    """
    shifted_dates = np.array(num_days_to_shift, dtype=np.dtype('M8[D]'))
    for i, x in enumerate(num_days_to_shift):
        shifted_dates[i] = min(dates) + datetime.timedelta(days=int(x))

    return shifted_dates


def write_to_csv_file(file_name, data):
    """
    Write data to a csv file. Data should be a list of lists, where each row is a list
    :param file_name: CSV file name to write to
    :param data: data to write to file, function assumes correct format
    :return:
    """
    with open(file_name, 'w', newline='') as data_file:
        data_writer = csv.writer(data_file)
        for row in data:
            data_writer.writerow(row)
