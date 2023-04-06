from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt

db_path = "sqlite:///Resources/hawaii.sqlite"
engine = create_engine(db_path)
Base = automap_base()
Base.prepare(autoload_with=engine)

measure = Base.classes.measurement
stat = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
    )


@app.route('/api/v1.0/precipitation')
def precip():
    session = Session(bind=engine)
    
    earliest_date = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    
    results = session.query(measure.date, measure.prcp).\
        filter(measure.date > earliest_date).all()
    
    session.close()
    
    list = []
    for date, prcp in results:
        dict = {}
        dict['date'] = date
        dict['prcp'] = prcp

        list.append(dict)

    return jsonify(list)

@app.route('/api/v1.0/stations')
def station():
    session = Session(bind=engine)
    
    results = session.query(measure.station, func.count(measure.station)).\
        group_by(measure.station).\
        order_by(func.count(measure.station).desc()).\
        all()
    
    session.close()
    
    list = []
    for station, count in results:
        dict = {}
        dict['station'] = station
        dict['count'] = count

        list.append(dict)

    return jsonify(list)

@app.route('/api/v1.0/tobs')
def temp():
    session = Session(bind=engine)

    station = 'USC00519281'
    
    results = session.query(func.min(measure.tobs), func.max(measure.tobs), func.avg(measure.tobs)).\
        group_by(measure.station).\
        filter(measure.station == station).all()
    
    session.close()
    
    list = []
    for min, max, avg in results:
        dict = {}
        dict['min'] = min
        dict['max'] = max
        dict['avg'] = avg

        list.append(dict)

    return jsonify(list)

@app.route('/api/v1.0/<start>')
def start(start):
    session = Session(bind=engine)
    
    results = session.query(func.min(measure.tobs), func.max(measure.tobs), func.avg(measure.tobs)).\
        filter(measure.date >= start).all()
    
    session.close()
    
    list = []
    for min, max, avg in results:
        dict = {}
        dict['min'] = min
        dict['max'] = max
        dict['avg'] = avg

        list.append(dict)

    return jsonify(list)

@app.route('/api/v1.0/<start>/<end>')
def endstart(start, end):
    session = Session(bind=engine)
    
    results = session.query(func.min(measure.tobs), func.max(measure.tobs), func.avg(measure.tobs)).\
        filter(measure.date >= start, measure.date < end).all()
    
    session.close()
    
    list = []
    for min, max, avg in results:
        dict = {}
        dict['min'] = min
        dict['max'] = max
        dict['avg'] = avg

        list.append(dict)

    return jsonify(list)

if __name__ == '__main__':
    app.run(debug=True)
