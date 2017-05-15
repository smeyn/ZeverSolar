#ZeverSolar
The ZeverSolar inverters have a (small) web site. Opening that page displays the current
readings for that website.
The Python application directly accesses the webserver,extracts the current readings
and stores them in a SqlLite Db.

The plot application (plotZever.py) creates a simple plot of the generation data.

Prerequisite: docopt.py
