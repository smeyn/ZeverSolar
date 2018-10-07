# ZeverSolar

The ZeverSolar inverters have a (small) web server. Opening that page displays the
current readings for that website.
The Python application directly accesses the webserver, extracts the current readings
and stores them in a SqlLite Db.

Please note that unlike, for example (/solmoller/eversolar-monitor)[https://github.com/solmoller/eversolar-monitor], this script interacts with the HTTP Web server and not the serial, Telnet or other connections ZeverSolar might operate on.

The plot application (plotZever.py) creates a simple plot of the generation data.

Prerequisite: docopt.py


## Initial setup (initialise the database)

    python zever.py -initDB

## Run the data collector

    python zever.py <url of inverter web server>

## Plot today's data


   python plotZever.py --today
