#TO DO : 1) Replace pd portion with sqlalchemy
#		 2) Try to figure out how to get the Table in raw_spectra into model.py
#		 3) Now that all the data has been added to the db, how is it gonna get updated?
#		 	=> Implemented for raw_spectra, next for available_dates and available_columns
#		 	=> Best thing to do is create a method that chooses between update and add
#		 	#SOLVED:Instead of update method, just use delete method
#		 4) Get all the ids in the db accounted for
#		 5) Get all payloads to React working just for completeness. However, in React, ingest from db.

from flask import Flask, jsonify, request
import model,services,repository
from sqlalchemy.engine import reflection
from sqlalchemy import Table,MetaData,Column,select
import orm
orm.start_mappers()
metadata = MetaData()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///2019scada.db', echo = True)
get_session = sessionmaker(bind=engine)
session = get_session()

app = Flask(__name__)

@app.route("/available_dates",methods=['POST'])
def available_dates():
	data = request.json
	repo = repository.SqlAlchemyRepository(session)
	dates = engine.table_names()
	services.availabledates(repo,dates)
	return jsonify(Dates=dates)
	
@app.route("/available_columns",methods=['POST'])
def available_columns():
	data = request.json
	repo = repository.SqlAlchemyRepository(session)
	columns = services.availablecolumns(repo,engine)
	return jsonify(Columns=columns)

@app.route("/arima_forecast",methods=['POST'])
def arima_forecast():
	data = request.json
	repo = repository.SqlAlchemyRepository(session)
	getColumns = Table(str(data['indicsvfiles']), metadata, autoload=True, autoload_with=engine)
	selectedAmp = select(from_obj=getColumns, columns=[Column(c) for c in [str(data['indicolumns'])]])
	selectedTime = select(from_obj=getColumns, columns=[Column(c) for c in ['TIME']])
	timeSpec,ampSpec = services.arimaforecast(repo,str(data['indicsvfiles']),selectedAmp,selectedTime)
	return jsonify(Time=timeSpec,Amplitude=ampSpec)

@app.route("/raw_spectra",methods=['POST'])
def raw_spectra():
	data = request.json
	repo = repository.SqlAlchemyRepository(session)
	getColumns = Table(str(data['indicsvfiles']), metadata, autoload=True, autoload_with=engine)
	selectedAmp = select(from_obj=getColumns, columns=[Column(c) for c in [str(data['indicolumns'])]])
	selectedTime = select(from_obj=getColumns, columns=[Column(c) for c in ['TIME']])
	timeSpec,ampSpec = services.rawspectra(repo,selectedAmp,selectedTime)
	return jsonify(Time=timeSpec,Amplitude=ampSpec)
	
@app.route("/kaiser_resp",methods=['POST'])
def kaiser_resp():
	data = request.json
	repo = repository.SqlAlchemyRepository(session)
	freq,resp = services.kaiserresp(repo,float(data['kaibeta']))
	return jsonify(Frequency=freq,Response=resp)

@app.route("/windowed_fft",methods=['POST'])
def windowed_fft():
	repo = repository.SqlAlchemyRepository(session)
	freq,resp = services.windowedfft(repo)
	return jsonify(Frequency=freq,Response=resp)

@app.route("/power_spectra",methods=['POST'])
def power_spectra():
	repo = repository.SqlAlchemyRepository(session)
	freq,Pxx_den = services.powerspectra(repo)
	return jsonify(PowerSpectra=Pxx_den,Response=resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 8080,debug=True)