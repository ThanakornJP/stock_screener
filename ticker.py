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
