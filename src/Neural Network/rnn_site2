import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')
os.environ["KERAS_BACKEND"] = "torch"
import keras
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import TimeSeriesSplit
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from model_preparation.import_model_data import model_df



#Create work Dataframe
df = model_df[['time', 'occupied_count', 'siteID']]
df = df[df['siteID'] == '2']
df.drop('siteID', axis=1, inplace=True)

#Create a Dataframe for the max and min datetime
df['index'] = pd.to_datetime(df['time'])
df = df.set_index(df['index']).resample('H').ffill()
df = df[['occupied_count']]
df = df.rename(columns={'occupied_count': 'value'})

null_vals = df.isnull().sum()
print('Null values in the target column {}'.format(null_vals))


#Transform data to hour by hour for every day

def transform_to_hour_cols(series):
    df = pd.DataFrame()

    start = series.index.min()
    end = series.index.max()
    
    df['year'] = series.index.year
    df['month'] = series.index.month
    df['day'] = series.index.day
    df['hours'] = series.index.hour
    df['loads'] = series.values
    
    df = df.set_index(['year', 'month', 'day', 'hours'], append=True).unstack()
    df = df.groupby(['year', 'month', 'day']).sum()
    
    df.reset_index(inplace=True)
    df.drop(['year', 'month', 'day'], axis=1, inplace=True)
    
    date_list = pd.date_range(start=start, end=end, freq='D').strftime('%Y-%m-%d')
    
    df.index = pd.DatetimeIndex(date_list, name='date')
    
    return df

day_utilization = transform_to_hour_cols(df['value'])
day_utilization.head()

#make life easier
day_utilization.columns = ["h"+ str(x) for x in range(0, 24)]

#isolate the original series of data
utilization_univar = df['value']

fig, axs = plt.subplots(1,2, figsize=(20,8))

#we will plot the last 30 and 90 days
lags = [30*24, 90*24]

for ax, lag in zip(axs.flatten(), lags):
    plot_acf(utilization_univar, ax=ax, lags=lag)
plt.plot()

plots = len(day_utilization.columns)
fig, axs = plt.subplots(int(plots/2), 2, figsize=(15, 2*plots))

for hour, ax in zip(day_utilization.columns, axs.flatten()):
        plot_acf(day_utilization.loc[:,hour], ax=ax, lags=60)
        ax.set_title('Autocorrelation hour ' + str(hour))
plt.plot()

plots = len(day_utilization.columns)
fig, axs = plt.subplots(int(plots/2), 2, figsize=(15, 2*plots))

for hour, ax in zip(day_utilization.columns, axs.flatten()):
        plot_pacf(day_utilization.loc[:,hour], ax=ax, lags=60)
        ax.set_title('Partial Autocorrelation hour ' + str(hour))
plt.plot()

def normalize_df(data):
    
    #normalize the dataset for working with the lstm nn
    scaler = MinMaxScaler().fit(data.values)
    data_normd = scaler.transform(data.values)
    
    #return as dataframe
    data = pd.DataFrame(data_normd, index=data.index, columns=data.columns)
    
    return data, scaler

#normalize the utilization dataframe
day_utilization_normed, scaler = normalize_df(day_utilization)

def split_sequences(sequences, n_steps, extra_lag=False, long_lag_step=7, max_step=30, idx=0, multivar=False):
    
    #if not adding extra lag features adjust max_step and n_steps to aling
    if not extra_lag:
        max_step=n_steps
        n_steps+=1
        
    
    X, y = list(), list()
    for i in range(len(sequences)):
        
        # find the end of this pattern
        #end_ix = i + n_steps
        end_ix = i + max_step
        
        #create a list with the indexes we want to include in each sample
        slices = [x for x in range(end_ix-1,end_ix-n_steps, -1)] + [y for y in range(end_ix-n_steps, i, -long_lag_step)]
        
        #reverse the slice indexes
        slices = list(reversed(slices))
        
        # check if we are beyond the dataset
        if end_ix > len(sequences)-1:
            break


        # gather input and output parts of the pattern
        seq_x = sequences[slices, :]
        seq_y = sequences[end_ix, :]

        X.append(seq_x)
        y.append(seq_y)
        
    X = np.array(X)
    y = np.array(y)
    
    if multivar:
        #unstack the 3rd dimension and select the first element(utilization load)
        y = y[:,idx]
    
    return X, y

#create the supervised learning problem
n_steps = 21

X, Y = split_sequences(day_utilization_normed.values, n_steps, extra_lag=True, long_lag_step=7, max_step=60, idx=0, multivar=False)
print(X.shape, Y.shape)
X[:5], Y[:5]

###define an LSTM model
#takes in parallel inputs and outputs an equal number of parallel outputs
def lstm_parallel_out(n_lags, n_hours, cells=50, learning_rate=5e-3):
    
    #define the model
    model = keras.models.Sequential()
    model.add(keras.layers.LSTM(cells, activation='relu', return_sequences=True, input_shape=(n_lags, n_hours)))
    model.add(keras.layers.LSTM(int(cells/2), activation='relu'))
    model.add(keras.layers.Dropout(0.3))
    model.add(keras.layers.Dense(n_hours))
    
    #define the learning rate
    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    
    #compile model
    model.compile(optimizer=optimizer, loss='mae', metrics=["mae", "mse"])
    
    return model

def crossval_testbench(X, y, n_crossvals, epochs=5, verbose=0):
    
    n_hours = X.shape[-1]
    n_features = X.shape[1]
    
    tscv = TimeSeriesSplit(n_splits=n_crossvals)

    #initalize lists to capture the output
    predictions = []
    actuals = []


    #run the LSTM model on each of the time series splits
    for train, test in tscv.split(X, y):
        
        #initalize the lstm model
        lstm_base = lstm_parallel_out(n_features, n_hours, learning_rate=5e-3)
        
        #fit the model
        lstm_base.fit(X[train], y[train], epochs=epochs, verbose=verbose, shuffle=False)
        
        #make predictions
        predict = lstm_base.predict(X[test], verbose=verbose)


        #inverse transform the predictions and actual values
        prediction = scaler.inverse_transform(predict)
        actual = scaler.inverse_transform(y[test].copy())

        #save the results in a list
        predictions.append(prediction)
        actuals.append(actual)
        
    predictions = np.array(predictions)
    actuals = np.array(actuals)
    
    return predictions, actuals

preds, actuals = crossval_testbench(X, Y, 2, epochs=150, verbose=1)

preds.shape, actuals.shape

from sklearn.metrics import mean_absolute_error as mae 

def mean_absolute_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return mae(y_true, y_pred) 

#MAE for a specific hour
error_h0 = mean_absolute_error(actuals[0,:5,0], preds[0, :5,0])
print(f'MAE for Hour 0: {round(error_h0, 2)}')

crossvals = actuals.shape[0]
hours = actuals.shape[2]

errors_crossvals = list()
for crossval in range(crossvals):
    errors_hourly = [mean_absolute_error(actuals[crossval, :, hour], preds[crossval, :, hour]) for hour in range(hours)]
    errors_crossvals.append(errors_hourly)
    
errors = pd.DataFrame(errors_crossvals)
errors['mean'] = errors.mean(axis=1)
errors.index.name='crossval set'
errors.columns.name='hours'
errors

plt.figure(figsize=(8,6))
plt.plot(errors.drop(columns='mean').T)
plt.title('MAPE per hourly prediction')
plt.legend(errors.index, title='crossval set')
plt.xlabel('Hour of the day')
plt.ylabel('MAPE')
plt.show()

def train_test_split(df, split_date):
    
    
    train_date = pd.Timestamp(split_date).strftime('%Y-%m-%d')
    test_date = (pd.Timestamp(split_date) + timedelta(1)).strftime('%Y-%m-%d')
    
    df_train = df[:train_date]
    df_test = df[test_date:]
    
    return df_train, df_test

train, test = train_test_split(day_utilization, '2020-12-31')

print(f'Training start date {train.index.min()} end date {train.index.max()}')
print(f'Training start date {test.index.min()} end date {test.index.max()}')

train_norm, scalar = normalize_df(train)
test_norm = scalar.transform(test)

#create the supervised learning problem
n_steps = 21

X_train, Y_train = split_sequences(train_norm.values, n_steps, extra_lag=True, long_lag_step=7, max_step=60, idx=0, multivar=False)

print(f'Training Set X {X_train.shape} and Y {Y_train.shape}')

test_set = np.vstack([train_norm.values[-60:], test_norm])
print(f'Dimensions of the test set with training data needed for predictions: {test_set.shape}')

X_test, Y_test = split_sequences(test_set, n_steps, extra_lag=True, long_lag_step=7, max_step=60, idx=0, multivar=False)

print(f'Testing Set X {X_test.shape} and Y {Y_test.shape}')

n_features=X_train.shape[1]
n_hours=X_train.shape[2]
#initalize the lstm model
lstm_eval = lstm_parallel_out(n_features, n_hours, learning_rate=5e-3)
        
#fit the model
lstm_eval.fit(X_train, Y_train, epochs=350, verbose=1, shuffle=False)
        
#check predictions on the train set
train_predictions = lstm_eval.predict(X_train, verbose=1)

#run predictions on test data
test_predictions = lstm_eval.predict(X_test, verbose=1)

train_preds = scalar.inverse_transform(train_predictions)
test_preds = scalar.inverse_transform(test_predictions)
Y_train = scalar.inverse_transform(Y_train)
Y_test = scalar.inverse_transform(Y_test)

train_error = pd.DataFrame([mean_absolute_error(Y_train[:, hour], train_preds[:, hour]) for hour in range(hours)], columns=['train'])
test_error = pd.DataFrame([mean_absolute_error(Y_test[:, hour], test_preds[:, hour]) for hour in range(hours)], columns=['test'])

errors = pd.concat([train_error, test_error], axis=1)
errors.index.name = 'hour'
errors.plot()

test_df = pd.DataFrame(test_preds).stack()
Y_test_df = pd.DataFrame(Y_test).stack()

preds_df = pd.concat([Y_test_df, test_df], axis=1)
preds_df.columns = ['actual', 'predicted']

preds_df.index = pd.DatetimeIndex(pd.date_range(start='2021-01-01 00:00:00', end='2021-09-14 23:00:00', freq='H'))

fig = plt.figure(figsize=(10,10))

for week in range(36):

    fig.add_subplot()
    preds_df.iloc[week*7*24:(week+1)*7* 24].plot()
    plt.title(f'utilization profile for 2021 Week: {week+1}')
