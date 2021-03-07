# Import Dependencies
import numpy as np
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from flask import Flask, jsonify

# Database Setup
#################################################
# Create engine and inspector
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
inspector = inspect(engine)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################

# Flask Setup
app = Flask(__name__)

@app.route('/')
def index():
    return (
        f'<h1>Available routes:</h1>'
        f'<ul>'
            f'<li>/api/v1.0/precipitation</li>'
            f'<li>/api/v1.0/stations</li>'
            f'<li>/api/v1.0/tobs</li>'
            f'<li>/api/v1.0/&lt;start> - replace &lt;start> with the following date format: YYYY-MM-DD</li>'
            f'<li>/api/v1.0/&lt;start>/&lt;end> - replace &lt;start> and &lt;end> with the following date format: YYYY-MM-DD</li>'
        f'</ul>'
        )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query
    query = session.query(Measurement.date, Measurement.prcp).all()
    # Close our session
    session.close()
    # Create a dictionary from the query data and append to a result list
    result = []
    for date, prcp in query:
        query_dict = {}
        query_dict['date'] = date
        query_dict['prcp'] = prcp
        result.append(query_dict)
    # Return a JSON of query results
    return jsonify(result)

@app.route('/api/v1.0/stations')
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query
    query = session.query(Station.station).all()
    # Close our session
    session.close()
    # Convert list of tuples into normal list
    result = list(np.ravel(query))
    # Return a JSON of query results
    return jsonify(result)

@app.route('/api/v1.0/tobs')
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Calculate timedelta using datetime module
    most_recent_date = session.query(func.max(Measurement.date)).all()
    most_recent_date = dt.datetime.strptime(most_recent_date[0][0], '%Y-%m-%d')
    time_delta = most_recent_date - dt.timedelta(days=365)
    # Query
    query = session.query(Measurement.tobs).filter(Measurement.date > time_delta).all()
    # Close our session
    session.close()
    # Convert list of tuples into normal list
    result = list(np.ravel(query))
    # Return a JSON of query results
    return jsonify(result)

@app.route('/api/v1.0/<start>')
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date > start).all()
    # Close our session
    session.close()
    # Create a dictionary from the query data and append to a result list
    result = []
    for tmin, tavg, tmax in query:
        query_dict = {}
        query_dict['minimum_temperature'] = tmin
        query_dict['average_temperature'] = tavg
        query_dict['maximum_temperature'] = tmax
        result.append(query_dict)
    # Return a JSON of query results
    return jsonify(result)

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    # Close our session
    session.close()
    # Create a dictionary from the query data and append to a result list
    result = []
    for tmin, tavg, tmax in query:
        query_dict = {}
        query_dict['minimum_temperature'] = tmin
        query_dict['average_temperature'] = tavg
        query_dict['maximum_temperature'] = tmax
        result.append(query_dict)
    # Return a JSON of query results
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)


