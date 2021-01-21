class AvailableDates:
	def __init__(self,dates:str):
		self.dates=dates
		
class AvailableColumns:
	def __init__(self,columns:str):
		self.columns=columns
		
class ArimaForecast:
	def __init__(self,time:str,amplitude:int):
		self.time=time
		self.amplitude=amplitude
		
class RawSpectra:
	def __init__(self,time:str,amplitude:int):
		self.time=time
		self.amplitude=amplitude
		
class KaiserResp:
	def __init__(self,frequency:int,response:int):
		self.frequency=frequency
		self.response=response
		
class NyqFs:
	def __init__(self,nyqfs:int):
		self.nyqfs=nyqfs
		
class KaiBeta:
	def __init__(self,kaibeta:int):
		self.kaibeta=kaibeta
		
class Window:
	def __init__(self,window:int):
		self.window=window
		
class WindowedFFT:
	def __init__(self,frequency:int,response:int):
		self.frequency=frequency
		self.response=response
		
class PowerSpectra:
	def __init__(self,frequency:int,spectra:int):
		self.frequency=frequency
		self.spectra=spectra