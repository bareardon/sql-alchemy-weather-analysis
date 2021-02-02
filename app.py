
# Import dependencies 
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Create an app
app = Flask(__name__)

# Set up database and create engine 
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

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
    welcome():
    """List all available app routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )
    

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
    results = session.query(Measurement.date, Measurement.prcp).all()
    return f""


@app.route("/api/v1.0/stations")
def stations():

    return f""

@app.route("/api/v1.0/tobs")
def tobs():

@app.route("//api/v1.0/<start> and /api/v1.0/<start>/<end>)
def start():

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
