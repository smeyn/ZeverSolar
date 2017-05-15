"""Plot Zever Data
Usage:
  plotZever [--today]

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
from datetime import datetime, timedelta


def plot(arguments):
    conn = sqlite3.connect('zeverData.db')
    c = conn.cursor()
    sql = "SELECT * FROM inverterData"
    fToday = arguments['--today']
    if fToday:
        lower = str(datetime.now().date())
        upper =  str(datetime.now().date() + timedelta(days=1))
        sql = sql + ' WHERE date>= "'+lower+ '" AND date< "'+ upper+'"'
    data={}

    for row in c.execute(sql ):
        #print(row)
        id = row[1]
        if not id in data:
            data[id]={'ts':[], 'current':[], 'total':[]}
        #print(row[0])
        dt = parser.parse(row[0])
        data[id]['ts'].append(dt)
        data[id]['current'].append(row[2])
        data[id]['total'].append(row[3])


    for id in data:
        #print(data[id]['current'])
        plt.plot(data[id]['ts'], data[id]['current'])

    if  fToday:
        locator = mdates.HourLocator()
    else:
        locator = mdates.AutoDateLocator()

    plt.gca().xaxis.set_major_formatter(mdates.AutoDateFormatter(locator ))

    plt.gcf().autofmt_xdate()

    plt.ylabel(('Watt'))

    plt.show()

if __name__ == '__main__':
    conn = sqlite3.connect('zeverData.db')
    arguments = docopt(__doc__)
    print(arguments)
    plot(arguments)