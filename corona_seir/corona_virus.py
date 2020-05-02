"""
This class contains the relevant data for the corona virus. Where possible, experimental data was gathered from
multiple sources, and averaged.
# fatality_rate 1.2, 0.36, 0.1 IFR vs CFR https://www.cebm.net/covid-19/global-covid-19-case-fatality-rates/,
https://www.medrxiv.org/content/10.1101/2020.03.05.20031773v2,
https://www.medrxiv.org/content/10.1101/2020.04.14.20062463v1.full.pdf

# generation_time (serial interval) https://www.ijidonline.com/article/S1201-9712(20)30119-3/pdf,
https://www.medrxiv.org/content/10.1101/2020.02.19.20025452v3.full.pdf

# no_symptoms https://www.zmescience.com/medicine/iceland-testing-covid-19-0523/

# r0 2.2-2.7 or 4.7-6.6 https://wwwnc.cdc.gov/eid/article/26/7/20-0282_article, https://www.medrxiv.org/content/10.1101/2020.02.07.20021154v1

# time_presymptomatic for transmission and sigma/incubation period https://www.medrxiv.org/content/10.1101/2020.03.08.20032946v1.full.pdf

# eigenvalue cal/ doubling time https://hal.archives-ouvertes.fr/hal-00657584/document page 15
"""
import math


class CoronaVirus(object):

    def __init__(self, fatality_rate=.0036, generation_time=4.18, incubation_period=5.2, no_symptoms=0.35, r0=2.2,
                 time_presymptom=2.5, find_factor=10):
        # Experimental/Research gathered data
        self._fatality_rate = fatality_rate
        self._generation_time = generation_time
        self._incubation_period = incubation_period
        self._no_symptoms = no_symptoms
        self._r0 = r0
        self._time_presymptom = time_presymptom
        self._find_factor = find_factor

        # Calculated data
        self._sigma = 1.0 / (self._incubation_period - self._time_presymptom)
        self._gamma = 1.0 / (2.0 * (self._generation_time - 1.0 / self._sigma))
        self._find_ratio = (1.0 - self._no_symptoms) / self._find_factor
        self._beta = self._r0 * self._gamma
        # Eigenvalue solution r1
        self._r1 = 0.5 * (-(self._sigma + self._gamma) +
                          math.sqrt((self._sigma + self._gamma) ** 2 + 4 * self._sigma * self._gamma * (
                        self._r0 - 1)))
        self.doubling_time = (math.log(2.0, math.e) / self._r1)


    @property
    def beta(self):
        return self._beta

    @beta.setter
    def beta(self, value):
        self._beta = value
    @property
    def fatality_rate(self):
        return self._fatality_rate

    @fatality_rate.setter
    def fatality_rate(self, rate):
        self._fatality_rate = rate

    @property
    def find_factor(self):
        return self._find_factor

    @find_factor.setter
    def find_factor(self, factor):
        self._find_factor = factor
        self.find_ratio = (1.0 - self._no_symptoms) / self._find_factor

    @property
    def find_ratio(self):
        return self._find_ratio

    @find_ratio.setter
    def find_ratio(self, ratio):
        self._find_ratio = ratio

    @property
    def gamma(self):
        return self._gamma

    @gamma.setter
    def gamma(self, value):
        self._gamma = value
        self.beta = self.r0 * self._gamma

    @property
    def generation_time(self):
        return self._generation_time

    @generation_time.setter
    def generation_time(self, value):
        self._generation_time = value
        self.gamma = 1.0 / (2.0 * (self._generation_time - 1.0 / self.sigma))

    @property
    def r0(self):
        return self._r0

    @r0.setter
    def r0(self, value):
        self._r0 = value
        self.beta = self._r0 * self.gamma

    @property
    def sigma(self):
        return self._sigma

    @sigma.setter
    def sigma(self, value):
        self._sigma = value
        self.gamma = 1.0 / (2.0 * (self.generation_time - 1.0 / self._sigma))

    @property
    def time_presymptom(self):
        return self._time_presymptom

    @time_presymptom.setter
    def time_presymptom(self, days):
        self._time_presymptom = days
        self.sigma = 1.0 / (5.2 - self._time_presymptom)