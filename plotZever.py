"""Plot Zever Data
Usage:
  plotZever [--today] [--from startDate --to endDate [--totals] ]

Options:
  -h --help     show this
  --today       only plot today
"""

import sqlite3
import time
import datetime
from docopt import docopt

#port numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from dateutil import parser
from datetime import datetime, timedelta, date


def buildDateQuery (arguments):
    sql = "SELECT  date, SN, PAC_W,  E_TODAY, Status FROM inverterData"
    fToday = arguments['--today']
    if fToday:
        lower = str(datetime.now().date())
        upper = str(datetime.now().date() + timedelta(days=1))
        sql = sql + ' WHERE date>= "' + lower + '" AND date< "' + upper + '"'
    else:
        leadIn = ' WHERE '
        if arguments['startDate']:
            fromDt = parser.parse(arguments['startDate'])
            sql = sql + ' WHERE date>= "' + str (fromDt)
            leadIn = ' AND '
        if arguments['endDate']:
            toDt = parser.parse(arguments['endDate'])
            sql = sql + leadIn + ' date< "' + str(toDt) + '"'
    return sql

def plotDetailed(arguments):
    conn = sqlite3.connect('zeverData.db')
    c = conn.cursor()
    sql = buildDateQuery(arguments)

    data = {}

    for row in c.execute(sql):
        # print(row)
        id = row[1]
        if not id in data:
            data[id] = {'ts': [], 'current': [], 'total': []}
        # print(row[0])
        dt = parser.parse(row[0])
        data[id]['ts'].append(dt)
        data[id]['current'].append(row[2])
        data[id]['total'].append(row[3])

    for id in data:
        # print(data[id]['current'])
        plt.plot(data[id]['ts'], data[id]['current'])

    if arguments['--today']:
        locator = mdates.HourLocator()
    else:
        locator = mdates.AutoDateLocator()

    plt.gca().xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))

    plt.gcf().autofmt_xdate()

    plt.ylabel(('Watt'))

    plt.show()

def plotTotals(arguments):
    """plot day totals only"""
    conn = sqlite3.connect('zeverData.db')
    c = conn.cursor()
    sql = buildDateQuery(arguments)
    data = {}

    for row in c.execute(sql):
        #SELECT  date, SN, PAC_W,  E_TODAY, Status FROM inverterData
        id = row[1]
        if not id in data:
            data[id] = {}
        # print(row[0])
        dt = parser.parse(row[0]).date()
        data[id][dt] = row[3] # overwrite with the latest value

    #fig, ax = plt.subplots()
    for id in data:
        xData = [dt for dt in data[id]]
        ticks =[str(dt )for dt in data[id]]
        yData = [ data[id][dt] for dt in data[id]]
        plt.bar(range(len(yData)),yData, align='center')
        plt.xticks(range(len(yData)), ticks)
        #plt.bar(xData, yData)
        print(xData)

    locator = mdates.DateLocator()
    #plt.gca().xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
    #plt.gcf().autofmt_xdate()
    plt.ylabel(('kWh'))
    plt.show()


def plot(arguments):
    if (arguments['--totals']):
        plotTotals(arguments)
    else:
        plotDetailed(arguments)

if __name__ == '__main__':
    #conn = sqlite3.connect('zeverData.db')
    arguments = docopt(__doc__)
    print(arguments)
    plot(arguments)