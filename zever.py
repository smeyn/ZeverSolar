"""Collect generation data from a ZeverSolar inverter
Usage:
  zever <URL> [--verbose]
  zever --initDB

Options:
  -h --help     show this
  -v --verbose  print output
  --initDB       initialise the DB
"""

import requests
import time
from datetime import datetime
from docopt import docopt
import sqlite3
import msvcrt
import sys

def kbfunc():
   x = msvcrt.kbhit()
   if x:
      ret = ord(msvcrt.getch())
   else:
      ret = 0
   return ret

def query_yes_no(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def processZeverResponse(content):
    """take the response from the Zever Web server and parse it"""
    parts = content.split('\n')
    results = {
        'enable_wifi': parts[0],
        'Registry Key': parts[3],
        'Hardware Version': parts[4],
        'Software Version': parts[5],
        'Time': parts[6]
    }
    if (parts[1] == '0') or (parts[1] == 3):
        results['Serial Number'] = parts[2]
    else:
        results['Registry ID'] = parts[2]

    if parts[7].startswith('OK'):
        results['Zevercloud communication'] = 'ok'
    else:
        results['Zevercloud communication'] = 'error'

    row = int(parts[8])
    item = 9
    inverterTable = []  # tb
    for i in range(5):
        if i < row:
            inverterTable.append({
                'SN': parts[item],
                'PAC(W)': parts[item + 1],
                'E_Today(KWh)': parts[item + 2],
                'Status': parts[item + 3]
            })
            item += 4
    results['inverter'] = inverterTable

    meter = {}
    meter['status'] = parts[item]
    results['meter'] = {}
    if parts[item].startswith('OK'):
        item += 1
        meter['m_p'] = parts[item]
        item += 1
        meter['m_in'] = parts[item]
        item += 1
        meter['m_out'] = parts[item]
        item += 1
        meter['m_meter'] = parts[item]

    return results

def collectData(arguments, conn):
    url = arguments['<URL>'] + '/home.cgi'

    interval = 30 #(seconds)
    while(True):
        if kbfunc():
            break

        response = requests.get(url=url)
        content = response.text
        result = processZeverResponse(content)
        for inverterData in result['inverter']:
            #(date text, SN text, PAC_W int,  E_TODAY real, Status text)
            params = (str(datetime.now()), inverterData['SN'],inverterData['PAC(W)'],inverterData['E_Today(KWh)'],inverterData['Status'])
            sql = 'INSERT INTO inverterData VALUES(?,?,?,?,?)'
            conn.execute(sql, params)
            conn.commit()

        print (result)
        time.sleep(interval)

def initDB(arguments, conn):
    print('Initialising DB - all data are getting lost')
    if query_yes_no('Do you want to proceed and delete all data'):
        c = conn.cursor()
        # Create table
        c.execute('''CREATE TABLE inverterData
                 (date text, SN text, PAC_W int,  E_TODAY real, Status text)''')
        conn.commit()
        print ('DB Initalised')
    else:
        print("DB not initialised")

if __name__ == '__main__':
    conn = sqlite3.connect('zeverData.db')
    arguments = docopt(__doc__)
    print(arguments)
    if arguments['--initDB']:
        initDB(arguments, conn)
    else:
        collectData(arguments, conn)
    conn.close()
