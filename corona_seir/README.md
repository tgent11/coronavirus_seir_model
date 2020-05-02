# coronavirus SEIR model
This is a basic model to calculate deaths and cases for the US and its states.  

## Other models
* This project is based on: https://github.com/coronafighter/coronaSEIR

## Disclaimer
This is not a scientific or medical tool. Use at your own risk. BETA! There might be serious bugs.  

## Features
* SEIR epidemic model
* Reduced R0 after a certain amount of days to account for containment measures.
* Delays to allow for lagging official data etc.
* hopefully easily readable code

## Installation / Requirements / Documentation
Needs Python 3.x installed. Tested on Windows.

Run the model with: python run_model.py

## Sources
# fatality_rate 1.2, 0.36, 0.1 IFR vs CFR https://www.cebm.net/covid-19/global-covid-19-case-fatality-rates/,
https://www.medrxiv.org/content/10.1101/2020.03.05.20031773v2,
https://www.medrxiv.org/content/10.1101/2020.04.14.20062463v1.full.pdf

# generation_time (serial interval) https://www.ijidonline.com/article/S1201-9712(20)30119-3/pdf,
https://www.medrxiv.org/content/10.1101/2020.02.19.20025452v3.full.pdf

# no_symptoms https://www.zmescience.com/medicine/iceland-testing-covid-19-0523/

# r0 2.2-2.7 or 4.7-6.6 https://wwwnc.cdc.gov/eid/article/26/7/20-0282_article, https://www.medrxiv.org/content/10.1101/2020.02.07.20021154v1

# time_presymptomatic for transmission and sigma/incubation period https://www.medrxiv.org/content/10.1101/2020.03.08.20032946v1.full.pdf

# eigenvalue cal/ doubling time https://hal.archives-ouvertes.fr/hal-00657584/document page 15


## License
MIT license
