import model,repository
from scipy import signal
from scipy.fftpack import fft,fftshift,fftfreq
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARIMAResults
import pandas as pd
import numpy as np

def availabledates(repo:repository.AbstractRepository,dates):
	repo.delete(model.AvailableDates)
	for i in range(len(dates)):
		if str(dates[i])[0] == '2':
			repo.add(model.AvailableDates(dates[i]))
	repo.commit()
	
def availablecolumns(repo:repository.AbstractRepository,engine):
	tarikh = repo.query(model.AvailableDates.dates)
	connection = engine.connect()
	topDateColumns = pd.read_sql_table(tarikh[0][0],connection)
	topDateColumnsList = topDateColumns.columns.tolist()
	repo.delete(model.AvailableColumns)
	for i in range(len(topDateColumnsList)):
		repo.add(model.AvailableColumns(topDateColumnsList[i]))	
	repo.commit()
	return topDateColumnsList

def arimaforecast(repo:repository.AbstractRepository,colName,selectedAmp,selectedTime):
	ampMentah = repo.query(selectedAmp)
	timeMentah = repo.query(selectedTime)
	forecastTime = []
	newtime = timeMentah[len(timeMentah)] + datetime.timedelta(seconds=60)
	for i in range(9):
		newtime = newtime + datetime.timedelta(seconds=60)
		forecastTime.append(newtime)
	model_fit =  ARIMAResults.load(colName+str(model.pkl))
	prediction = model_fit.forecast()[10]
	repo.delete(model.ArimaForecast)
	for i in range(len(prediction)):
		repo.add(model.ArimaForecast(forecastTime[i][0],prediction[i][0]))
	repo.commit()
	return forecastTime,prediction
	
def rawspectra(repo:repository.AbstractRepository,selectedAmp,selectedTime):
	ampMentah = repo.query(selectedAmp)
	timeMentah = repo.query(selectedTime)
	repo.delete(model.RawSpectra)
	for i in range(len(ampMentah)):
		repo.add(model.RawSpectra(timeMentah[i][0],ampMentah[i][0]))
	repo.commit()
	return timeMentah,ampMentah
	
def kaiserresp(repo:repository.AbstractRepository,kaibeta):
	amplitude = repo.query(model.RawSpectra.amplitude)
	nyqfs = np.floor(len(amplitude))
	window = signal.kaiser(nyqfs,beta=kaibeta,sym=False)
	A = fft(window) / (len(window)/2.0)
	freq = np.linspace(-nyqfs, nyqfs, len(A))
	response = 20 * np.log10(np.abs(fftshift(A / abs(A).max())))
	repo.delete(model.KaiserResp)
	repo.delete(model.Window)
	repo.delete(model.NyqFs)
	repo.delete(model.KaiBeta)	
	for i in range(len(freq)):
		repo.add(model.KaiserResp(freq[i],response[i]))
	for i in range(len(window)):
		repo.add(model.Window(window[i]))
	repo.add(model.NyqFs(nyqfs))
	repo.add(model.KaiBeta(kaibeta))
	repo.commit()
	return freq,response
	
def windowedfft(repo:repository.AbstractRepository):
	amplitude = repo.query(model.RawSpectra.amplitude)
	window = repo.query(model.Window.window)
	A = fft(np.array(amplitude) * np.array(window)) / (len(window)/2.0)
	nyqfs = repo.query(model.NyqFs.nyqfs)
	freq = fftfreq(len(amplitude))*nyqfs*2
	response = 20 * np.abs(A)
	repo.delete(model.WindowedFFT)	
	for i in range(len(freq[0])):
		repo.add(model.WindowedFFT(freq[0][i],response[i][0]))	
	repo.commit()
	return freq,response	
	
def powerspectra(repo:repository.AbstractRepository):
	amplitude = repo.query(model.RawSpectra.amplitude)
	seglength = len(amplitude)
	denom = 2
	coeff = 1
	frequency, spectra = signal.welch(amplitude, seglength,window=('kaiser',repo.query(model.KaiBeta.kaibeta)),scaling='spectrum',average='mean',nfft=seglength*coeff)
	repo.delete(model.PowerSpectra)
	for i in range(len(frequency)):
		repo.add(model.PowerSpectra(frequency[i],spectra[0][i]))
	repo.commit()
	return frequency,spectra
