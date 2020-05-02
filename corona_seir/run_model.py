import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets  # Cursor
import matplotlib.dates
import matplotlib.ticker
import datetime

import data_utilities
from constants import INIT_INFECTED, QUARANTINE_R1, DATA_OFFSET, INIT_R0, DAYS0
from corona_virus import CoronaVirus
from country_data import CountryData
from seir_model import solve, model_changing_beta, calculate_deaths, calculate_reported_cases

def run_model(country_data, virus, plot, save_data):
    """
    Main driver function to run the SEIR model to predict virus cases and deaths
    :param country_data: CountryData() object
    :param virus: Virus object
    :return:
    """
    # SEIR model to predict cases, deaths
    # Date, Susceptible, Exposed, Infected, Recovered
    days, susceptible, exposed, infected, recovered = solve(model_changing_beta, country_data.population,
                                                            INIT_INFECTED, virus)

    reported_cases = calculate_reported_cases(infected, virus=virus)
    predicted_deaths = calculate_deaths(days, recovered, virus=virus)
    # Shift dates to best align model
    data_offset = data_utilities.get_offset_x(country_data.deaths, predicted_deaths, data_offset=DATA_OFFSET)  # match model day to real data day for deaths curve  todo: percentage wise?
    model_days = days - data_offset
    #
    model_days_shifted = data_utilities.model_to_world_time(model_days, country_data.dates)

    # Plot
    if plot:
        fig = plt.figure(dpi=75, figsize=(20,16))
        ax = fig.add_subplot(111)
        ax.fmt_xdata = matplotlib.dates.DateFormatter('%Y-%m-%d')  # higher date precision for cursor display
        ax.set_yscale("log", nonposy='clip')

        # Actual Data
        ax.plot(country_data.dates, country_data.reported_cases, 'o', color='orange', alpha=0.5, lw=1, label='cases actually detected in tests')
        ax.plot(country_data.dates, country_data.deaths, 'x', color='black', alpha=0.5, lw=1, label='actually deceased')

        # Model data
        ax.plot(model_days_shifted, infected, 'r--', alpha=0.5, lw=1, label='Infected (realtime)')
        ax.plot(model_days_shifted, reported_cases, color='orange', alpha=0.5, lw=1, label='Found cumulated: "cases" Curve Fitted')
        ax.plot(model_days_shifted, predicted_deaths, 'k', alpha=0.5, lw=1, label='Deaths Curve Fitted')

        ax.set_xlabel('Time /days')
        ax.set_ylim(bottom=1.0)
        ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
        ax.xaxis.set_minor_locator(matplotlib.dates.WeekdayLocator())
        ax.yaxis.set_major_locator(matplotlib.ticker.LogLocator(numticks=10, base=10.0, subs=(1.0,)))
        ax.yaxis.set_minor_locator(matplotlib.ticker.LogLocator(numticks=10, base=10.0,
                                                            subs=np.arange(2, 10) * .1))


        ax.grid(linestyle=':')  #b=True, which='major', c='w', lw=2, ls='-')

        legend = ax.legend(title='COVID-19 SEIR model: ' + ' (beta)\n')
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)
        cursor = matplotlib.widgets.Cursor(ax, color='black', linewidth=1 )
        plt.show()

    if save_data:
        today = datetime.datetime.now()
        today_str = "{}_{}_{}".format(today.year, today.month, today.day)
        actual_data_filename = "{}_actual_data_{}_.csv".format(country_data.name, today_str)
        model_data_filename = "{}_model_R0={}_R1={}_IFR={}_{}_.csv".format(country_data.name, INIT_R0, QUARANTINE_R1, virus.fatality_rate, today_str)

        # Format data for csv file
        header = ['name', 'date', 'predicted cases', 'predicted deaths', 'r0 value', 'fatality rate']
        model_data = []
        model_data.append(header)
        for i in range(0, len(model_days_shifted)):
            row = []
            row.append(country_data.name)
            row.append(str(model_days_shifted[i]))
            row.append(reported_cases[i])
            row.append(predicted_deaths[i])
            row.append(INIT_R0)
            row.append(virus.fatality_rate)
            model_data.append(row)

        data_utilities.write_to_csv_file(actual_data_filename, country_data.csv_data)
        data_utilities.write_to_csv_file(model_data_filename, model_data)

    # text output
    print("corona_virus.sigma: %.3f  1/corona_virus.sigma: %.3f    corona_virus.gamma: %.3f  1/corona_virus.gamma: %.3f" % (corona_virus.sigma, 1.0/corona_virus.sigma, corona_virus.gamma, 1.0/corona_virus.gamma))
    print("doubling0 every ~%.1f" % corona_virus.doubling_time, "days")
    print("total predicted deaths: {}".format(predicted_deaths[-1]))
    print("actual deaths: {}".format(country_data.deaths[-1]))
    print("lockdown measures start:", model_days_shifted[DAYS0])


if __name__ == '__main__':
    name = 'United States'
    # Show a quick plot of the data?
    plot = True
    # Save data in excel .csv file?
    save_data = False
    country_data = CountryData(name=name, county=False, update_data=True)
    # Corona Virus object, change fatality_rate if needed
    corona_virus = CoronaVirus(r0=INIT_R0, fatality_rate=.0036, no_symptoms=0.35, time_presymptom=2.5, find_factor=30)
    # Main run function
    run_model(country_data=country_data, virus=corona_virus, plot=plot, save_data=save_data)
