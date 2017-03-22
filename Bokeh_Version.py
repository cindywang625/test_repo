__author__ = 'Cindy.Wang'
"""
This module is used to create graphs from the Dashboard for Building Performance Lab using Bokeh.
Date: 11/4/2016
"""
#For Yorkville Library Time Series (Electricity)
#Elec_time_series and Fuel_time_series both have OAT in the same graph as Fuel/Electricity use and contains their respective legends.


#TODO: create function to find the best parameter for electricity and fuel seperately. Can math be used? is the best parameter given.
'''
http://stackoverflow.com/questions/41172227/bokeh-layout-for-plot-and-widget-arrangement
    https://github.com/bokeh/bokeh/blob/0.12.4/examples/howto/layouts/dashboard.py
https://blog.ometer.com/
'''
import numpy as np
import bokeh.plotting as bk
from bokeh.io import gridplot
from math import pi
from bokeh.io import curdoc, vform
import pandas as pd
from bokeh.models import LinearAxis, Range1d
from bokeh.charts import Bar, output_file, show
from pandas import DataFrame as df
from bokeh.plotting import figure, show
from bokeh.models import Range1d
from bokeh.palettes import Reds6
from bokeh.palettes import Oranges4
from bokeh.palettes import Greens6
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn



dates = ['7/31/2014', '8/31/2014', '9/30/2014', '10/31/2014', '11/30/2014', '12/31/2014', '1/31/2015', '2/28/2015',
         '3/31/2015', '4/30/2015', '5/31/2015', '6/30/2015', '7/31/2015', '8/31/2015', '9/30/2015', '10/31/2015',
         '11/30/2015', '12/31/2015', '1/31/2016', '2/29/2016', '3/31/2016', '4/30/2016', '5/31/2016', '6/30/2016']
temp = [76.9437, 75.1606, 70.7929, 60.4991, 45.6132, 40.8425, 29.8991, 24.1328, 37.4478, 52.9555, 66.6022, 71.2865,
        79.0559, 79.4356, 74.3958, 58.7216, 53.2139, 50.4697, 36.0472, 38.714, 49.0472, 53.4194, 63.3125, 73.6936]
temp1 = [76.9437, 75.1606, 70.7929, 60.4991, 45.6132, 40.8425, 29.8991, 24.1328, 37.4478, 52.9555, 66.6022, 71.2865,
         79.0559, 79.4356, 74.3958, 58.7216, 53.2139, 50.4697, 36.0472, 38.714, 49.0472, 53.4194, 63.3125, 73.6936]
temp1.sort()
elec = [0.0440867, 0.0422825, 0.0365335, 0.0191006, 0.0206212, 0.0207748, 0.02266, 0.0215611, 0.0216979, 0.0235252,
        0.0293219, 0.034076, 0.0386776, 0.0429352, 0.0361416, 0.0235508, 0.0210843, 0.0119062, 0.0128275, 0.0129652,
        0.0128337, 0.0128337, 0.0164837, 0.0319173]
fuel = [0.747602, 1.00529, 1.15193, 29.6758, 175.574, 23.4635, 252.35, 301.397, 170.813, 44.7661, 4.82141, 2.33729,
        2.14101, 2.09258, 2.13174, 4.04792, 21.4527, 72.6187, 248.614, 229.513, 127.981, 103.275, 55.5285, 7.07844]
elec_xcp = 0
elec_ycp = -.002
elec_slope = .0005
heatload = 0
coolload = 5.20
totalcon = 18.57
perheat = 0
percool = 28
base = 72
ccp = 61
tpo = 24
site_breakdown = [0, 48, 0, 52]
source_breakdown = [0, 74, 0, 26]
CO2e = 3
EUI = 7
fheatload = 49676.60
fcoolload = 0
ftotalcon = 56700.17
fperheat = 88
fpercool = 0
fbase = 12
fhcp = 59
ftpo = 24
ecool = 5.38
ebase = 0
eheat = 9.2
ecoolsen = 5.37
fcool = 5.38
fbasel = 0
fheat = 9.2
fcoolsen = 5.37
avuse = 9
avbase = 72
avheat = 6.7
avcool = 28
avbase_value = 6.7
avheat_value = 0
avcool_value = 2.6
favbase_value = 3.5
favheat_value = 24.8
favcool_value = 0
favuse = 28
favbase = 12
favheat = 88
favcool = 0


def twop_model(temps, ycp, xcp, slope):
    yint = ycp - xcp*slope
    ylist = []
    for temp in temps:
        yval = yint + slope*temp
        ylist.append(yval)
#Yfunc = [Yint + slope1*val for val in temps]
    return ylist
def threepc_model(temps, ycp, xcp, slope):
    yint = ycp - xcp*slope
    ylist = []
    for temp in temps:
        if temp >= xcp:
            yval = yint+ slope*temp
            ylist.append(yval)
        else:
            yval = ycp
            ylist.append(yval)
    return ylist
def threeph_model(temps, ycp, xcp, ls):
    yint = ycp - xcp*ls
    ylist = []
    for temp in temps:
        if temp <= xcp:
            yval = yint + ls*temp
            ylist.append(yval)
        else:
            yval = ycp
            ylist.append(yval)
    return ylist
def fourp_model(temps, ycp, xcp, rs, ls):
    yint = ycp - xcp*ls
    yint2 = ycp - xcp*rs
    xlist, ylist = [], []

    for inc, temp in enumerate(temps):
        if temp <= xcp:
            yval = yint + ls*temp
            ylist.append(yval)
            xlist.append(temp)
    ylist.append(ycp)
    xlist.append(xcp)

    for inc, temp in enumerate(temps):
        if temp > xcp:
            yval2 = yint2 + rs*temp
            ylist.append(yval2)
            xlist.append(temp)
    return xlist, ylist
def fivep_model(temps, ycp, xcp, xcp2, rs, ls):
    yint = ycp - xcp*ls
    yint2 = ycp - xcp2*rs
    xlist, ylist = [], []

    for inc, temp in enumerate(temps):
        if temp <= xcp:
            yval= yint + ls*temp
            ylist.append(yval)
            xlist.append(temp)
    ylist.append(ycp)
    xlist.append(xcp)
    ylist.append(ycp)
    xlist.append(xcp2)
    for inc, temp in enumerate(temps):
        if temp > xcp2:
            yval2 = yint2 + rs*temp
            ylist.append(yval2)
            xlist.append(temp)

    return xlist, ylist

#electricty values
ylist = twop_model(temp, elec_ycp, elec_xcp, elec_slope)
ylist_3pc = threepc_model(temp1, 0.0182554231393, 60.8424987793, 0.00138974147610794)
ylist_3ph = threeph_model(temp1, 0.0242279062294, 71.0924987793, 0.000189980955804015)
xlist_4p, ylist_4p = fourp_model(temp1, 0.0161211387896, 56.5924987793, 0.00118099982684539, -0.000130228955176554)
xlist_5p, ylist_5p = fivep_model(temp1, 0.0170248394144, 41.0924987793, 57.5924987792968, 0.00119764747823224,
                                 -0.000277989152365653)
#fuel values
ylist_fuel = twop_model(temp, 370.374797813, 0, -5.1438693088908)
ylist_3pc_fuel = threepc_model(temp1, 121.185444819, 40.8424987793, -3.63070032723704)
ylist_3ph_fuel = threeph_model(temp1, 9.30700698188, 59.0924987793, -8.37153455136918)
xlist_4p_fuel, ylist_4p_fuel = fourp_model(temp1, 26.7945920276, 57.3424987793, -1.29551723917029, -8.23054124837103)
xlist_5p_fuel, ylist_5p_fuel = fivep_model(temp1, 25.3067355118, 57.8424987793, 63.0924987792968, -1.83893856458461,
                                           -8.10468517077283)

# output to static HTML file
bk.output_file("Dashboard.html", title="dashboard")

#p1 = electricity values
p1 = bk.figure(title="Electricity", width=300, height=250)
p1.title.background_fill_color = '#6baed6'
data = {
    "Model":['Yearly Average Usage \n(kWh/sqf)', 'Estimated Average\n Baseload', 'Estimated Average Heating',
           'Estimated Average Cooling'],
    "Usage":[avuse, avbase, avheat, avcool]}
source = ColumnDataSource(data)
columns = [
    TableColumn(field="Model", title=" "),
    TableColumn(field="Usage", title="  ")
]

p1 = DataTable(source=source, columns=columns)


p1a = bk.figure(title="Electricity", width=400, height=250)
p1a.hbar(y=[3, 2, 1], height=0.5, left=0,
        right=[avbase_value, avheat_value, avcool_value], color=['gray', 'orange', 'blue'])

p1b = bk.figure(title="Electricity", width=50, height=250)
data1 = dict(
    Usage1=[avbase_value, avheat_value, avcool_value]

)
source1 = ColumnDataSource(data1)
columns = [
    TableColumn(field="Usage1", title="kWh/sqf")
]
p1b = DataTable(source=source1, columns=columns)


#p2 = fuel values
p2 = bk.figure(title="Fuel", width=300, height=300)
p2.title.background_fill_color = '#fc9272'
data = dict(
    Model=['Yearly Average Usage \n(kWh/sqf)', 'Estimated Average\n Baseload', 'Estimated Average Heating',
           'Estimated Average Cooling'],
    Usage=[favuse, favbase, favheat, favcool]
)
source = ColumnDataSource(data)
columns = [
    TableColumn(field="Model", title=" "),
    TableColumn(field="Usage", title="  ")
]

p2 = DataTable(source=source, columns=columns)

p2a = bk.figure(title="Electricity", width=400, height=250)
p2a.hbar(y=[3, 2, 1], height=0.5, left=0,
        right=[favbase_value, favheat_value, favcool_value], color=['gray', 'orange', 'blue'])


p2b = bk.figure(title="Electricity", width=50, height=250)
data2 = dict(
    Usage1=[favbase_value, favheat_value, favcool_value]
)
source2 = ColumnDataSource(data2)
columns = [
    TableColumn(field="Usage1", title="kWh/sqf")
]
p2b = DataTable(source=source2, columns=columns)

#p3 = time series for electricity
p3 = bk.figure(title="Time Series", x_range=dates, width=800)
p3.title.background_fill_color = '#6baed6'
p3.line(x=dates, y=elec, color="blue", legend="Electricity Use")
p3.y_range = Range1d(0, 0.05)
p3.yaxis.axis_label = "Electricity Use (kWh/Day/Sqf)"
p3.extra_y_ranges = {"Outside Air Temperature (F)": Range1d(start=0, end=90)}
p3.add_layout(LinearAxis(y_range_name="Outside Air Temperature (F)"), 'right')
p3.line(x=dates, y=temp, y_range_name="Outside Air Temperature (F)", color="black", legend="OAT")
p3.xaxis.axis_label = "Date"
p3.xaxis.major_label_orientation = pi/4

#p4 = time series for fuel
p4 = bk.figure(title="Time Series", x_range=dates, width=800)
p4.title.background_fill_color = '#fc9272'
p4.line(x=dates, y=fuel, color="red", legend="Fuel Use")
p4.y_range = Range1d(0, 400)
p4.yaxis.axis_label = "Fuel Use (BTU/Day/Sqf)"
p4.extra_y_ranges = {"Outside Air Temperature (F)": Range1d(start=0, end=90)}
p4.add_layout(LinearAxis(y_range_name="Outside Air Temperature (F)"), 'right')
p4.line(x=dates, y=temp, y_range_name="Outside Air Temperature (F)", color="black", legend="OAT")
p4.xaxis.axis_label = "Date"
p4.xaxis.major_label_orientation = pi/4

#p5 = parameter model for electricity
p5 = bk.figure(title="Yorkville Branch Library", width=800, height=600)
p5.title.background_fill_color = '#6baed6'
p5.xaxis.axis_label = "OAT"
p5.yaxis.axis_label = "kWh (Daily Avg/sqf)"
p5.circle(x=temp, y=elec, color="blue")
p5.line(x=temp1, y=ylist_3pc, color="black")

#p6 = parameter model for fuel
p6 = bk.figure(title="Yorkville Branch Library", width=800, height=600)
p6.title.background_fill_color = '#fc9272'
p6.xaxis.axis_label = "OAT"
p6.yaxis.axis_label = "BTU (Daily Avg/sqf)"
p6.circle(x=temp, y=fuel, color="red")
p6.line(x=temp1, y=ylist_3ph_fuel, color="black")

ylabels = ['Cooling\n Change\n Point', '', 'Baseload', '', 'Heating\n Sensitivity', '', 'Cooling\n Sensitivity']


#p7 = lean metrics for electricity
p7 = bk.figure(title="Electricity LEAN Metrics", y_range=ylabels, width=800, height=500)
p7.title.background_fill_color = '#6baed6'

p7.hbar(y=[1, 1, 1], height=0.5, left=0,
        right=[10, 7.5, 2.5], color=['green', 'orange', 'red'])
p7.hbar(y=[3, 3, 3], height=0.5, left=0,
        right=[10, 7.5, 2.5], color=['green', 'orange', 'red'])
p7.hbar(y=[5, 5, 5], height=0.5, left=0,
        right=[10, 7.5, 2.5], color=['green', 'orange', 'red'])
p7.hbar(y=[7, 7, 7], height=0.5, left=0,
        right=[10, 7.5, 2.5], color=['green', 'orange', 'red'])
p7.inverted_triangle(x=[ecool, ebase, eheat, ecoolsen], y=[1, 3, 5, 7], size=20, color='white')

#p8 = lean metrics for fuel
p8 = bk.figure(title="Fuel LEAN Metrics", width=800, height=500)
p8.title.background_fill_color = '#fc9272'

p8.hbar(y=[1, 1, 1], height=0.5, left=0,
        right=[10, 7.5, 2.5], color=['green', 'orange', 'red'])
p8.hbar(y=[3, 3, 3], height=0.5, left=0,
        right=[10, 7.5, 2.5], color=['green', 'orange', 'red'])
p8.hbar(y=[5, 5, 5], height=0.5, left=0,
        right=[10, 7.5, 2.5], color=['green', 'orange', 'red'])
p8.hbar(y=[7, 7, 7], height=0.5, left=0,
        right=[10, 7.5, 2.5], color=['green', 'orange', 'red'])
p8.yaxis.axis_label = " " \
                      ""
p8.inverted_triangle(x=[fcool, fbase, fheat, fcoolsen], y=[1, 3, 5, 7], size=20, color='white')

#p9 = electricity coefficient
p9 = bk.figure(title="Coefficient")
p9.title.background_fill_color = '#6baed6'

data = dict(
    Model=['Estimated Heating Load', 'Estimated Cooling Load', 'Estimated Total Consumption', 'Percent Heating',
           'Percent Cooling', 'Baseload', 'Cooling Change Point', 'Total Points Observed'],
    Usage=[heatload, coolload, totalcon, perheat, percool, base, ccp, tpo],
    Units=['kWh/sqf', 'kWh/sqf', 'kWh/sqf', '%', '%', '%', 'F', 'Months']
)
'''
df = pd.DataFrame(data, columns=["Model", "Usage", "Units"])
p9 = pd.pivot_table(df, index=["Model"], values=["Usage", "Units"])
'''
source = ColumnDataSource(data)
columns = [
    TableColumn(field="Model", title="Model Used"),
    TableColumn(field="Usage", title="Estimated Usage"),
    TableColumn(field="Units", title="Units")
]

p9 = DataTable(source=source, columns=columns, width=800, height=250)

#p10 = fuel coefficient
p10 = bk.figure(title="Coefficient")
p10.title.background_fill_color = '#fc9272'
data = dict(
    Model=['Estimated Heating Load', 'Estimated Cooling Load', 'Estimated Total Consumption', 'Percent Heating',
          'Percent Cooling', 'Baseload', 'Cooling Change Point', 'Total Points Observed'],
    Usage=[fheatload, fcoolload, ftotalcon, fperheat, fpercool, fbasel, fhcp, ftpo],
    Units=['BTU/sqf', 'BTU/sqf', 'BTU/sqf', '%', '%', '%', 'F', 'Months']

)
source = ColumnDataSource(data)
columns = [
    TableColumn(field="Model", title="Model Used"),
    TableColumn(field="Usage", title="Estimated Usage"),
    TableColumn(field="Units", title="Units")
]

p10 = DataTable(source=source, columns=columns, width=800, height=250)


#p11 = combined energy for elec and fuel
p11 = bk.figure(title="Electricity & Fuel Models (Site Energy)", width=800)

p11.y_range = Range1d(0, 350)
p11.yaxis.axis_label = "BTU (Daily Avg/sqf)"
p11.line(x=temp1, y=ylist_3ph_fuel, color="red")
p11.circle(x=temp, y=fuel, color="red", legend="Fuel")
p11.extra_y_ranges = {"kbtu": Range1d(start=0, end=.08)}
p11.line(x=temp1, y=ylist_3pc, y_range_name="kbtu", color="blue")
p11.circle(x=temp, y=elec, y_range_name="kbtu", color="blue", legend="Electricity")
p11.xaxis.axis_label = "OAT"
p11.x_range = Range1d(10, 90)

#p12 = energy breakdown and co2 emissions
p12 = bk.figure(title="Energy Breakdown & CO2e Emissions")
mydf= df(
    dict(
        percent=site_breakdown,
        label=["District Steam", "Electricity", "Natural Gas", "Fuel Oil"],
        color=['aquamarine', 'cyan', 'salmon', 'crimson']
    )
)

p12 = Bar(mydf, values="percent", label="label", color="color", legend=False,
          title='Site Energy Breakdown', width=300)
p12.xaxis.axis_label = ' '

p12a = bk.figure(title="Energy Breakdown & CO2e Emissions")
mydf2 = df(
    dict(
        percent=source_breakdown,
        label=["District Steam", "Electricity", "Natural Gas", "Fuel Oil"],
        color=['aquamarine', 'cyan', 'salmon', 'crimson']
    )
)

p12a = Bar(mydf2, values="percent", label="label", legend=False, color="color",
          title='Source Energy Breakdown', width=300)
p12a.xaxis.axis_label = ' '

p12b = bk.figure(title="Energy Breakdown & CO2e Emissions")
data = {
    'sample': [1, 1, 1],
    'values': [25, 50, 25],
    'color': ['green', 'orange', 'red']
}

p12b = Bar(data, values='values', color='color', legend=False, stack='sample',
          title='EUI Rank', width=100)
p12b.inverted_triangle(x=[1], y=[EUI], size=30, color='black')
p12b.yaxis.axis_label = ' '

p12c = bk.figure(title="Energy Breakdown & CO2e Emissions")
data = {
    'sample': [1, 1, 1],
    'values': [25, 50, 25],
    'color': ['green', 'orange', 'red']
}

p12c = Bar(data, values='values', color='color', legend=False, stack='sample', title='CO2e/sqft Rank', width=120)
p12c.inverted_triangle(x=[1], y=[CO2e], size=30, color='black')
p12c.yaxis.axis_label = ' '

#set up the dashboard using gridplot
s = gridplot([[p1, p1a, p1b, p2, p2a, p2b], [p3, p4], [p5, p6], [p7, p8], [p9, p10], [p11, p12, p12a, p12b, p12c]], toolbar_location='left')
curdoc().add_root(s)
bk.show(s)
