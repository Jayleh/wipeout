import datetime as dt
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import numpy as np

# Database Setup
# Create engine
engine = create_engine("sqlite:///database/hawaii.sqlite")

# Declare Base
Base = automap_base()

# Use Base class to reflect database tables
Base.prepare(engine, reflect=True)

# Save references to measurements and stations tables
Measurement = Base.classes.measurements
Station = Base.classes.stations

# Create a session
session = Session(engine)

# Flask Setup
app = Flask(__name__)


@app.route("/")
def home():
    """
    List all available api routes.
    """
    print("Server received request for 'home' page...")
    return (
        f"<h1>Hawaii Climate API</h1>"
        f"Available Routes:<br>"
        f"<ul><li><a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a> — List "
        "of precipitation (prcp) data for 2017</li>"
        f"<li><a href='/api/v1.0/stations'>/api/v1.0/stations</a> — List of stations</li>"
        f"<li><a href='/api/v1.0/tobs'>/api/v1.0/tobs</a> — List of temperature "
        "observations (tobs) for 2017</li>"
        f"<li>/api/v1.0/start-date — List of the minimum, average, and max temperatures "
        "for a given start date to the latest date</li>"
        f"<li>/api/v1.0/start-date/end-date — List of the minimum, average, and max temperatures "
        "for a given start-end date range</li></ul>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query precipitation data from last year
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2017-01-01").all()

    # Create a list of dicts with `date` and `prcp` as the keys
    prcp_data = []
    for result in results:
        row = {}
        row["date"] = result[0]
        row["prcp"] = float(result[1])
        prcp_data.append(row)

    print("Server received request for 'precipitation' page...")
    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    # Query stations data
    results = session.query(Station.station, Station.name, Station.latitude,
                            Station.longitude, Station.elevation).all()

    # Create lists of dicts
    station_data = []
    for result in results:
        row = {}
        row["station"] = result[0]
        row["name"] = result[1]
        row["latitude"] = result[2]
        row["longitude"] = result[3]
        row["elevation"] = result[4]
        station_data.append(row)

    print("Server received request for 'stations' page...")
    return jsonify(station_data)


@app.route("/api/v1.0/tobs")
def tobs():
    # Query precipitation data from last year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2017-01-01").all()

    # Create a list of dicts with `date` and `tobs` as the keys
    tobs_data = []
    for result in results:
        row = {}
        row["date"] = result[0]
        row["tobs"] = float(result[1])
        tobs_data.append(row)

    print("Server received request for 'tobs' page...")
    return jsonify(tobs_data)


def daily_normals(a_date):
    """
    Grab min, avg, max temperatures for historic dates.
    """

    # Query to grab all historic temperatures by date
    temps = session.query(Measurement.tobs).\
        filter(Measurement.date.like(f"%{a_date}")).all()

    # Convert list of tuples into normal list
    temps = list(np.ravel(temps))

    # Calculate min, avg, and max temps, change to float to be json serializable
    min_temp = min(temps).astype(np.float)
    avg_temp = np.mean(temps).round(1).astype(np.float)
    max_temp = max(temps).astype(np.float)

    return min_temp, avg_temp, max_temp


@app.route("/api/v1.0/<start>")
def date(start):
    # Print request
    print("Server received request for 'date' page...")

    try:
        # Check to see if date format is correct
        dt.datetime.strptime(start, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": f"Invalid date format of '{start}'. "
                        "Format must be 'YYYY-MM-DD'."}), 404

    # Grab earliest date and latest date
    earliest_date = session.query(Measurement.date).order_by(Measurement.date).first()
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Check if date is in dataset
    if dt.datetime.strptime(start, "%Y-%m-%d") < dt.datetime.strptime(earliest_date[0], "%Y-%m-%d"):
        return jsonify({"error": f"Invalid date of '{start}'. "
                        f"Earliest date is {earliest_date[0]}."}), 404
    elif dt.datetime.strptime(start, "%Y-%m-%d") > dt.datetime.strptime(latest_date[0], "%Y-%m-%d"):
        return jsonify({"error": f"Invalid date of '{start}'. "
                        f"Latest date is {latest_date[0]}."}), 404

    # Query precipitation data from last year
    results = session.query(Measurement.date).\
        filter(Measurement.date >= start).all()

    # Convert list of tuples into normal list
    date_list = list(np.ravel(results))

    # Create month day list
    month_day_list = []

    for date in date_list:

        # Convert datetime to string
        a_date = dt.datetime.strptime(date, "%Y-%m-%d")

        # Grab only month and day
        month_day = f"{dt.datetime.strftime(a_date, '%m-%d')}"

        # Append month_day to list
        month_day_list.append(month_day)

    # Create lists to hold min, avg, and max temperatures
    min_temp_list = []
    avg_temp_list = []
    max_temp_list = []

    # Loop through each date in trip date list
    for date in month_day_list:

        # Pass date into daily_normals function
        min_temp, avg_temp, max_temp = daily_normals(date)

        # Append returns to lists
        min_temp_list.append(min_temp)
        avg_temp_list.append(avg_temp)
        max_temp_list.append(max_temp)

    # Create a dictionary from the row data and append to a list of temp_data
    temp_data = []
    for i, date in enumerate(date_list):
        row = {}
        row["date"] = date
        row["tmin"] = min_temp_list[i]
        row["tavg"] = avg_temp_list[i]
        row["tmax"] = max_temp_list[i]
        temp_data.append(row)

    return jsonify(temp_data)


@app.route("/api/v1.0/<start>/<end>")
def date_range(start, end):
    # Print request
    print("Server received request for 'date range' page...")

    try:
        # Check to see if date format is correct
        dt.datetime.strptime(start, "%Y-%m-%d")
        dt.datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": f"Invalid date format of '{start}/{end}'. "
                        "Format must be 'YYYY-MM-DD'."}), 404

    # Query precipitation data from last year
    results = session.query(Measurement.date).\
        filter(Measurement.date.between(start, end)).all()

    # Convert list of tuples into normal list
    date_list = list(np.ravel(results))

    # Create month day list
    month_day_list = []

    for date in date_list:

        # Convert datetime to string
        a_date = dt.datetime.strptime(date, "%Y-%m-%d")

        # Grab only month and day
        month_day = f"{dt.datetime.strftime(a_date, '%m-%d')}"

        # Append month_day to list
        month_day_list.append(month_day)

    # Create lists to hold min, avg, and max temperatures
    min_temp_list = []
    avg_temp_list = []
    max_temp_list = []

    # Loop through each date in trip date list
    for date in month_day_list:

        # Pass date into daily_normals function
        min_temp, avg_temp, max_temp = daily_normals(date)

        # Append returns to lists
        min_temp_list.append(min_temp)
        avg_temp_list.append(avg_temp)
        max_temp_list.append(max_temp)

    # Create a dictionary from the row data and append to a list of temp_data
    temp_data = []
    for i, date in enumerate(date_list):
        row = {}
        row["date"] = date
        row["tmin"] = min_temp_list[i]
        row["tavg"] = avg_temp_list[i]
        row["tmax"] = max_temp_list[i]
        temp_data.append(row)

    return jsonify(temp_data)


if __name__ == '__main__':
    app.run(debug=True)
