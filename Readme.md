#ZeverSolar

The ZeverSolar inverters have a (small) web site. Opening that page displays the current
readings for that website.
The Python application directly accesses the webserver,extracts the current readings
and stores them in a SqlLite Db.

The plot application (plotZever.py) creates a simple plot of the generation data.

Prerequisite: docopt.py

To run the data collector:

## initial setup (initialise the database)

    python zever.py -initDB

## run the data collector

    python zever.py <url of inverter web server>

## plot today's data


   python plotZever.py --today
