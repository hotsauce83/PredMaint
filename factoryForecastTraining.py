# grid search ARIMA parameters for time series
import warnings
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
import glob

from itertools import groupby
def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

# evaluate an ARIMA model for a given order (p,d,q) and return RMSE
def evaluate_arima_model(X, arima_order):
    # prepare training dataset
    X = X.astype('float32')
    train_size = int(len(X) * 0.50)
    train, test = X[0:train_size], X[train_size:].reset_index(drop=True)
    history = [x for x in train]
    # make predictions
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=arima_order)
        model_fit = model.fit(disp=0)
        yhat = model_fit.forecast()[0]
        predictions.append(yhat)
        history.append(test[t])
    # calculate out of sample error
    rmse = sqrt(mean_squared_error(test, predictions))
    return rmse

# evaluate combinations of p, d and q values for an ARIMA model
def evaluate_models(dataset, p_values, d_values, q_values):
    dataset = dataset.astype('float32')
    best_score, best_cfg = float("inf"), None
    for p in p_values:
        for d in d_values:
            for q in q_values:
                order = (p,d,q)
                try:
                    rmse = evaluate_arima_model(dataset, order)
                    if rmse < best_score:
                        best_score, best_cfg = rmse, order
                    print('ARIMA%s RMSE=%.3f' % (order,rmse))
                except:
                    continue
    print('Best ARIMA%s RMSE=%.3f' % (best_cfg, best_score))
    return best_cfg

#Identify columns that are nonstationary and append to boollist
boollist = []
series = pd.read_csv('2019ScadaData/2019-5-13.csv')
for i in range(2,len(series.columns)):
    boollist.append(all_equal(series[series.columns[i]].values))


scadacsvfiles = glob.glob("2019ScadaData/*.csv")
combined_csv = pd.concat([pd.read_csv(f) for f in scadacsvfiles ])

for i in range(2,len(combined_csv.columns)):
    dataset = combined_csv[combined_csv.columns[i]]
    # evaluate parameters
    p_values = range(0,13)
    d_values = range(0, 4)
    q_values = range(0, 13)
    warnings.filterwarnings("ignore")
    if boollist[i] == False:
        best_cfg = evaluate_models(dataset, p_values, d_values, q_values)
        model = ARIMA(dataset,best_cfg)
        model_fit = model.fit(disp=0)
        model_fit.save(str(combined_csv.columns[i])+'model.pkl')
        