# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 18:28:58 2020

@author: Joisel
"""


# import Dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func ,inspect
from flask import Flask, jsonify

#%%

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#%%

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

#%%

Measurement = Base.classes.measurement
Station = Base.classes.station

#%%

session = Session(engine)
inspector = inspect(engine)
inspector.get_table_names()

#%%

app = Flask(__name__)

#%%

@app.route("/")
def home():
    return("/api/v1.0/precipitation<br/>"
           "/api/v1.0/stations<br/>"
           "/api/v1.0/tobs<br/>"
           "/api/v1.0/2017-01-01<br/>"
           "/api/v1.0/2017-01-01/2017-01-09")

@app.route("/api/v1.0/precipitation")
def precipitation():
    results1 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>="2016-08-23").all()
    first_dict = list(np.ravel(results1))
    return jsonify(first_dict)
    
#%%

@app.route("/api/v1.0/stations")
def stations():
    results2 = session.query(Station.station, Station.name).all()
    sec_dict = list(np.ravel(results2))
    return jsonify(sec_dict)
#%%

@app.route("/api/v1.0/tobs")
def tobs():
    results3 = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date>="2016-08-23").\
            filter(Measurement.date<="2017-08-23").all()
    temp_dict = list(np.ravel(results3))
    return jsonify(temp_dict)

   

#%%
    
@app.route("/api/v1.0/<start>")
def start(start=None):

    from_start = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).group_by(Measurement.date).all()
    from_start_list=list(from_start)
    return jsonify(from_start_list)


#%% 
@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    between_dates = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
            filter(Measurement.date <= end).group_by(Measurement.date).all()
    between_dates_list=list(between_dates)
    return jsonify(between_dates_list)  


  
#%%
        
if __name__ == '__main__':
    app.run(debug=True)