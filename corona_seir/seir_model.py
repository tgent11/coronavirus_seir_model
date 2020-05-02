import scipy.integrate
import numpy as np
from data_utilities import delay
from constants import SYMPTOM_HOSPITAL_LAG, TIME_IN_HOSPITAL, COMMUNICATION_LAG, DAYS_TOTAL, TEST_LAG, \
QUARANTINE_R1, LIFTED_Q_R2, DAYS0, DELTA_R0, DAYS_Q_LIFTED


def calculate_deaths(days, recovered, virus):
    """
    This function calculates the deaths from a given virus based on the
    number of people who "recover" and the infection fatality rate.
    "Recovered" is a misnomer in this sense, because the fatality rate times the number
    of "recovered" is basically the number of deaths. After you're infected, you "recover" after a certain
    period of time which means you're healthy with immunity, or dead.
    :param days: Total number of days during infection
    :param recovered: Number of people who were infected, then recover, or die
    :param virus: Virus object which contains data such as fatality rate, gamma
    :return:
    """
    deaths = np.arange(DAYS_TOTAL)
    rprev = 0
    dprev = 0
    for i, x in enumerate(days):
        # Weird convergence issues with these LOC, check for really small values
        deaths[i] = dprev + virus.fatality_rate * (recovered[i] - rprev)
        rprev = recovered[i]
        dprev = deaths[i]

    time_infected = 1.0 / virus.gamma
    deaths = delay(deaths, - time_infected + virus.time_presymptom + SYMPTOM_HOSPITAL_LAG + TIME_IN_HOSPITAL + COMMUNICATION_LAG)  # deaths  from R

    return deaths

def calculate_reported_cases(infected, virus):
    """
    Use the virus "find ratio" to calculate the number of reported cases
    :param infected: Number of infected people
    :param virus: Virus object
    :return: type list - Number of reported cases
    """
    reported_cases = infected * virus.find_ratio
    reported_cases = delay(reported_cases, virus.time_presymptom + SYMPTOM_HOSPITAL_LAG + TEST_LAG + COMMUNICATION_LAG)  # found in tests and officially announced; from I
    # cumulate found --> cases
    reported_cases = np.cumsum(reported_cases)

    return reported_cases


def get_reproduction(dx, curr_r0):
    """
    Get new R0 value based on number of days that have passed.
    R0 changes if quarantine measures have been lifted
    :param dx: Current day of evaluation
    :param curr_beta: calculated with
    :return: float new R0 value
    """
    new_r0 = curr_r0
    if DAYS0 <= dx < DAYS_Q_LIFTED:
        return QUARANTINE_R1

    elif dx >= DAYS_Q_LIFTED:
        if curr_r0 < LIFTED_Q_R2:
            return curr_r0 + DELTA_R0
        else:
            return LIFTED_Q_R2

    return new_r0


def model_changing_beta(prev_soln, dx, population, virus):
    """
    SEIR model with a changing R0/beta value due to quarantining measures
    :param prev_soln: previous ODE solution
    :param dx: timestep
    :param population: total population
    :param virus: Virus object
    :return: solution to ODE delta values
    """
    # :param list x: Time step (days)
    # :param int N: Population
    s, e, i, r = prev_soln
    # Beta = r0 * gamma
    virus.r0 = get_reproduction(dx, virus.r0)

    ds = -virus.beta * s * i / population
    de = virus.beta * s * i / population - virus.sigma * e
    di = virus.sigma * e - virus.gamma * i
    dr = virus.gamma * i

    return ds, de, di, dr


def seir_model(prev_soln, dx, population, virus):
    """
    Solve the SEIR ODE
    :param prev_soln: previous ODE solution
    :param dx: timestep
    :param population: total population
    :param virus: Virus object
    :return: solution to ODE delta values
    """
    s, e, i, r = prev_soln

    ds = - virus.beta * s * i / population
    de = virus.beta * s * i / population - virus.sigma * e
    di = virus.sigma * e - virus.gamma * i
    dr = virus.gamma * i

    return ds, de, di, dr


def solve(model, population, init_infected, virus):
    """
    Main driver function for the model ode
    :param model: Function which contains the ode
    :param population: Total population
    :param init_infected: Number of people who start the simualtion infected
    :param virus: Virus object
    :return:
    """
    num_days = np.arange(DAYS_TOTAL)
    n0 = population - init_infected, init_infected, 0, 0  # S, E, I, R at initial step

    y_data_var = scipy.integrate.odeint(model, n0, num_days, args=(population, virus))

    s, e, i, r = y_data_var.T  # transpose and unpack

    return num_days, s, e, i, r  # note these are all lists



