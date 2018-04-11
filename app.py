from flask import Flask, jsonify
from sqlalchemy import create_engine, func
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
    return (
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation — List of precipitation (prcp) data for 2017<br/>"
        f"/api/v1.0/stations — List of stations<br/>"
        f"/api/v1.0/tobs — List of temperature observations (tobs) for 2017<br/>"
        f"/api/v1.0/start-date/end-date"
        f" — List of the minimum, average, and max temperatures "
        "for a given start or start-end range<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query precipitation data from last year
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2017-01-01").all()

    # Convert list of tuples into normal list
    # prcp_list = list(np.ravel(results))

    # Create a list of dicts with `date` and `prcp` as the keys
    prcp_data = []
    for result in results:
        row = {}
        row["date"] = result[0]
        row["prcp"] = float(result[1])
        prcp_data.append(row)

    print("Server received request for 'About' page...")
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

    print("Server received request for 'About' page...")
    return jsonify(station_data)


@app.route("/api/v1.0/tobs")
def tobs():
    # Query precipitation data from last year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2017-01-01").all()

    # Convert list of tuples into normal list
    # prcp_list = list(np.ravel(results))

    # Create a list of dicts with `date` and `tobs` as the keys
    tobs_data = []
    for result in results:
        row = {}
        row["date"] = result[0]
        row["tobs"] = float(result[1])
        tobs_data.append(row)

    print("Server received request for 'About' page...")
    return jsonify(tobs_data)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date_range():
    # jsonify(dictionary)
    pass


if __name__ == '__main__':
    app.run(debug=True)
