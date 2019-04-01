# ZeverSolar

The ZeverSolar inverters have a (small) web server. Opening that page displays the
current readings for that website.
The Python application directly accesses the webserver, extracts the current readings
and stores them in a SQLite Db.

Please note that unlike, for example solmoller's [eversolar-monitor](https://github.com/solmoller/eversolar-monitor), this script interacts with the HTTP Web server and not the serial, Telnet or other connections ZeverSolar might operate on.

The plot application (plotZever.py) creates a simple plot of the generation data.

Environment: Python 3, Pip 7+
Prerequisite: docopt.py

## Install Requirements

	pip install -r requirements.txt

## Initial setup (initialise the database)

	python zever.py -initDB
	
Note: if this line fails, delete all .db files in the directory and try again

## Run the data collector

	python zever.py <url_of_inverter_web_server>

## Plot today's data

	python plotZever.py --today

