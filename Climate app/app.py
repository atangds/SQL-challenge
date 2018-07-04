from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurements
Station = Base.classes.stations
session = Session(bind=engine)

from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
@app.route("/api/v1.0/home")
def home():
    return ("Welcome to Climate App v1.0!<br/><br/>"
            "Available Routes:<br/>"
            "/api/v1.0/stations<br/>"
            "/api/v1.0/precipitation<br/>"
            "/api/v1.0/tobs<br/>"
            "/api/v1.0/start(/end)"
    )

@app.route("/api/v1.0/stations")
def station():
    q1 = session.query(Station.station)
    return jsonify([_[0] for _ in q1.all()])

@app.route("/api/v1.0/precipitation")
def prcp():
    q2 = session.query(Measurement.date, func.group_concat(Measurement.station), func.group_concat(Measurement.prcp)).filter(Measurement.date > "2016-08-23").group_by(Measurement.date)
    d2 = {date: {s: p for s, p in zip(station.split(","), prcp.split(","))} for date, station, prcp in q2.all()}
    return jsonify(d2)

@app.route("/api/v1.0/tobs")
def tobs():
    q3 = session.query(Measurement.date, func.group_concat(Measurement.station), func.group_concat(Measurement.tobs)).filter(Measurement.date > "2016-08-23").group_by(Measurement.date)
    d3 = {date: {s: t for s, t in zip(station.split(","), tobs.split(","))} for date, station, tobs in q3.all()}
    return jsonify(d3)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start, end="2017-08-23"):
    tavg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date.between(start, end)).one()[0]
    tmax = session.query(func.max(Measurement.tobs)).filter(Measurement.date.between(start, end)).one()[0]
    tmin = session.query(func.min(Measurement.tobs)).filter(Measurement.date.between(start, end)).one()[0]
    d4 = {"start": start, "end": end, "avg_temp": tavg, "max_temp": tmax, "min_temp": tmin}
    return jsonify(d4)

if __name__ == "__main__":
    app.run(debug=True)
