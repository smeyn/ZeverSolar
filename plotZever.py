"""Plot Zever Data
Usage:
  plotZever [--today] [--from=startDate --to=endDate [--totals] ]

Options:
  -h --help     show this
  --today       only plot today
  --from=startDate   startdate in format yyyy-mm-dd
  --to=endDate       endDate  in format yyyy-mm-dd
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


def buildDateQuery (select, arguments, post="  ORDER BY date"):
    sql = select
    fToday = arguments['--today']
    if fToday:
        lower = str(datetime.now().date())
        upper = str(datetime.now().date() + timedelta(days=1))
        whereValue =  ' WHERE date >= "' + lower + '" AND date < "' + upper + '"'
        sql = sql + whereValue
    else:
        leadIn = ' WHERE '
        if arguments['--from']:
            fromDt = parser.parse(arguments['--from'])
            sql = sql + ' WHERE date>= "' + str (fromDt) +'" '
            leadIn = ' AND '
        if arguments['--to']:
            toDt = parser.parse(arguments['--to'])
            sql = sql + leadIn + ' date< "' + str(toDt) + '"'
    sql += post
    print(sql)
    return sql

def plotDetailed(arguments):
    conn = sqlite3.connect('zeverData.db')
    c = conn.cursor()
    sql = buildDateQuery("SELECT  date, SN, PAC_W,  E_TODAY, Status FROM inverterData", arguments )

    data = {}
    count=0
    for row in c.execute(sql):
        # print(row)
        count += 1
        id = row[1]
        if not id in data:
            data[id] = {'ts': [], 'current': [], 'total': []}
        # print(row[0])
        dt = parser.parse(row[0])
        data[id]['ts'].append(dt)
        data[id]['current'].append(row[2])
        data[id]['total'].append(row[3])
    if count == 0:
        print("No Data returned")
        return
    for id in data:
        # print(data[id]['current'])
        plt.plot(data[id]['ts'], data[id]['current'])

    if arguments['--today']:
        locator = mdates.HourLocator()
    else:
        locator = mdates.AutoDateLocator()

    plt.gca().xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))

    plt.gcf().autofmt_xdate()
    # work out title
    if arguments['--today']:
        plt.title(str(datetime.now()))
    elif arguments['--from']  or arguments['--to']:
        title = ' - '.join([arguments['--from'], arguments['--to']])
        plt.title(title)
    plt.ylabel(('Watt'))

    plt.show()

def plotTotals(arguments):
    """plot day totals only"""
    conn = sqlite3.connect('zeverData.db')
    c = conn.cursor()
    sql =  buildDateQuery("SELECT  date, SN, E_TODAY FROM inverterData",
                          arguments,
                          post =  " ORDER BY date ASC" )
    sql += " "
    data = {}
    print (sql)
    for row in c.execute(sql):

        #SELECT  date, SN, PAC_W,  E_TODAY, Status FROM inverterData
        id = row[1]
        if not id in data:
            data[id] = {}
        # print(row[0])
        dt = parser.parse(row[0]).date()
        if not (dt in data[id]) or (data[id][dt] < row[2]):
            data[id][dt] = row[2] # overwrite with the latest value

    #fig, ax = plt.subplots()
    for id in data:
        xData = [dt for dt in sorted(data[id])]
        ticks =[str(dt )for dt in data[id]]
        yData = [ data[id][dt] for dt in sorted(data[id])]
        print (yData)
        print (xData)
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