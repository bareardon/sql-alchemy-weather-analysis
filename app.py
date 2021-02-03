
# Import dependencies 
import numpy as np
import datetime as dt 
import pandas as pd 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create an app
app = Flask(__name__)

# Set up database and create engine 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station 

# Create session (link) from Python to the DB
session = Session(engine)

# Define static routes
@app.route("/")
def home():
    """List all available app routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )
 

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Query results to a dictionary using date as the key and prcp as the value.
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > year_ago).order_by(Measurement.date).all()

    session.close()

    # Convert list into a dictionary 
    prcp_data = []
    for date, prcp in precipitation:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_data.append(prcp_dict)

    # Return the JSON representation of your dictionary
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    total_stations = session.query(Station.station).all()
    all_stations = list(np.ravel(total_stations))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    # Query the dates and temperature observations of the most active station for the last year of data.
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    year_temperature = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= year_ago).all()

    # Return a JSON list of temperature observations (TOBS) for the previous year.
    active_station = list(np.ravel(year_temperature))
    return jsonify(active_station)
        
@app.route("//api/v1.0/<start>") 
def start(start):

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    start_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    calc_temps = list(np.ravel(start_results))
    return jsonify(calc_temps)

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
   
    end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    between_temps = list(np.ravel(end_results))
    return jsonify(between_temps)

# Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
