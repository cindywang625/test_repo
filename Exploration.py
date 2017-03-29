import pandas as pd
import numpy as np
from pandas import DataFrame

heatload = 0
coolload = 5.20
totalcon = 18.57
perheat = 0
percool = 28
base = 72
ccp = 61
tpo = 24



data = {
    "Model":['Estimated Heating Load', 'Estimated Cooling Load', 'Estimated Total Consumption', 'Percent Heating',
           'Percent Cooling', 'Baseload', 'Cooling Change Point', 'Total Points Observed'],
    "Usage":[heatload, coolload, totalcon, perheat, percool, base, ccp, tpo],
    "Units":['kWh/sqf', 'kWh/sqf', 'kWh/sqf', '%', '%', '%', 'F', 'Months']
}

df = pd.DataFrame(data, columns =['Model', 'Usage', 'Units'])
p = pd.pivot_table(df, index = ['Model', 'Units'], values = ['Usage'])
print p