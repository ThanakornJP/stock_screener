import urllib, json
import requests
import pylab
import plotly.offline as pyo 
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from pandas_datareader import data as pdr 
import yfinance as yf
from yahoo_fin import stock_info as si 
import numpy as np
import csv

def model(model):
    if model is None: 
        return None 
    else:
        symbols = set( symbol for symbol in model[0].values.tolist())
        del_set = set()
        sav_set = set()
        my_list = ['W','R','P','Q']
        for symbol in symbols:
            if len(symbol) > 4 and symbol[-1] in my_list:
                del_set.add(symbol)
            else:
                sav_set.add(symbol)
        return sav_set


def load(exchange):
    if exchange == 'snp':
        return pd.DataFrame(si.tickers_sp500())    
    elif exchange == 'nasdaq':
        return pd.DataFrame(si.tickers_nasdaq())
    else:
        return None


def save(df, model):
    with open(model, 'w') as f:
        for tick in df:    
            f.write(tick)
            f.write('\n')

def reload():
    save(model(load('snp')),'tick.snp.csv')
    save(model(load('nasdaq')),'tick.nasdaq.csv')

def getModelFromFile():
    dividend_with_info = pd.read_csv('dividends_with_info.nasdaq.csv')
    dividend_with_info['exchange'] = dividend_with_info['exchange'].fillna('')
    dividend_with_info['industry'] = dividend_with_info['industry'].fillna('')
    dividend_with_info['sector'] = dividend_with_info['sector'].fillna('')
    return dividend_with_info


def getModelFromFile():    
    df = pd.DataFrame(si.tickers_sp500())
    #df.rename(columns = {'0': 'tick' }, inplace = True)
    #df['tick'] = df['0']
    df.columns = ['tick']

    # if model == 'nasdaq':
    #     for ticker in pd.read_csv('tick.nasdaq.csv.1'):            
    #         dividend_table['tick'].append(ticker.strip())

    #     if len(dividends) < 1:        
    #         print("Skip " + ticker.strip() + "!")
    #         dividend_table['tick'].append(ticker.strip())
    #     df1 = model(load('tick.nasdaq.csv.1'))
    #     df2 = model(load('tick.nasdaq.csv.2'))
    #     df3 = model(load('tick.nasdaq.csv.3'))
    #     df4 = model(load('tick.nasdaq.csv.4'))
    #     df5 = model(load('tick.nasdaq.csv.5'))
    #     df = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)
    #     save(df,'dividends.nasdaq.csv')


# df1 = pd.DataFrame(si.tickers_sp500())
# df1.columns = ['tick']
# df1['exchange'] = 'snp5'
# df2 = pd.DataFrame(si.tickers_nasdaq())
# df = pd.concat([pd.DataFrame(si.tickers_sp500()), pd.DataFrame(si.tickers_nasdaq())], ignore_index=True)

#df = pd.DataFrame(si.tickers_sp500())
# df.columns = ['tick']
# print(df.head())
# print(df.tail())


dd1 = pd.read_csv('nasdaq-listed.csv')
print(dd1.head())
dt = pd.DataFrame()
dt['tick'] = dd1['Symbol']
dt['name'] = dd1['Company Name']
print(dt.tail()) 
print(dt.info())
# dd2 = pd.read_csv('nasdaq-listed.csv', skiprows=1)
# df = pd.concat([pd.DataFrame(si.tickers_sp500()), pd.DataFrame(si.tickers_nasdaq())], ignore_index=True)
# print(df)