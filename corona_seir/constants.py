"""
These are constants for the SEIR model. The indicated values can/should be tweaked as needed.
The other values should be left alone, unless better information is available.
"""
### -------------------------VALUES TO CHANGE----------------------------- ###
# Total days to model, 1 year is pretty good.
DAYS_TOTAL = 365
# Initial reproduction rate of the virus. USA ~2.5, OR ~ 1.4
INIT_R0 = 2.5
# Reproduction Value once lockdown measures start - estimated to be 0.95 or 1.0
QUARANTINE_R1 = 1
# Now lift the lockdown, set a new reproduction value. Or stay in quarantine: LIFTED_Q_R2 = QUARANTINE_R1
LIFTED_Q_R2 = QUARANTINE_R1
# When does the lockdown start? Change this based on output "lockdown measures start: ...."
DAYS0 = 74
# When does lockdown end?
DAYS_Q_LIFTED = DAYS0 + 75
### -------------------------------------------------------------------- ###

INIT_INFECTED = 1
DELTA_R0 = 0.0025 # Decrement R0 a little at a time during week before full lockdown or after lockdown ends
DATA_OFFSET = 'auto'  # position of real world data relative to model in whole days. 'auto' will choose optimal offset based on matching of deaths curves
TIME_IN_HOSPITAL = 12
COMMUNICATION_LAG = 2
TEST_LAG = 3
SYMPTOM_HOSPITAL_LAG = 5
HOSPITAL_ICU_LAG = 5