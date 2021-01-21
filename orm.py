import model

from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date,
    ForeignKey
)

from sqlalchemy.orm import mapper, relationship

metadata = MetaData()

availabledates = Table(
    'AvailableDates', metadata,
	Column('id', Integer, primary_key=True),
    Column('dates', String(255),nullable=False)
)

availablecolumns = Table(
    'AvailableColumns', metadata,
	Column('id', Integer, primary_key=True),
    Column('columns', String(255),nullable=False)
)

arimaforecast = Table(
    'ArimaForecast', metadata,
	Column('id', Integer, primary_key=True),
	Column('time', String(255),nullable=False),
    Column('amplitude',Integer,nullable=False)

rawspectra = Table(
    'RawSpectra', metadata,
	Column('id', Integer, primary_key=True),
	Column('time', String(255),nullable=False),
    Column('amplitude',Integer,nullable=False)
)

kaiserresp = Table(
    'KaiserResp', metadata,
	Column('id', Integer, primary_key=True),
	Column('frequency', Integer,nullable=False),
    Column('response',Integer,nullable=False)
)

nyqfs = Table(
    'NyqFs', metadata,
	Column('id', Integer, primary_key=True),
    Column('nyqfs',Integer,nullable=False)
)

kaibeta = Table(
    'KaiBeta', metadata,
	Column('id', Integer, primary_key=True),
    Column('kaibeta',Integer,nullable=False)
)


window = Table(
    'Window', metadata,
	Column('id', Integer, primary_key=True),
    Column('window',Integer,nullable=False)
)

windowedfft = Table(
    'WindowedFFT', metadata,
	Column('id', Integer, primary_key=True),
	Column('frequency', Integer,nullable=False),
    Column('response',Integer,nullable=False)
)

powerspectra = Table(
    'PowerSpectra', metadata,
	Column('id', Integer, primary_key=True),
	Column('frequency', Integer,nullable=False),
    Column('spectra',Integer,nullable=False)
)

def start_mappers():
	mapper(model.AvailableDates, availabledates)
	mapper(model.AvailableColumns, availablecolumns)
	mapper(model.ArimaForecast, arimaforecast)
	mapper(model.RawSpectra, rawspectra)
	mapper(model.KaiserResp, kaiserresp)
	mapper(model.NyqFs, nyqfs)
	mapper(model.Window, window)
	mapper(model.KaiBeta, kaibeta)
	mapper(model.WindowedFFT, windowedfft)
	mapper(model.PowerSpectra, powerspectra)