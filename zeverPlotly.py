"""Plot Zever Data using Plotly
Usage:
  zeverPlotly [--today]

Options:
  -h --help     show this
  --today       only plot today
"""

import sqlite3
import time
import datetime
from docopt import docopt
import plotly
from dateutil import parser
from datetime import datetime, timedelta





if __name__ == '__main__':
    conn = sqlite3.connect('zeverData.db')
    arguments = docopt(__doc__)
    print(arguments)
    plotly.tools.set_credentials_file(username='stephanmeyn', api_key='Rh3pgWgqtK92PR7yYz9A')
    #plot(arguments)