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


def filterOut(model):
    terminating_symbol = ['W','R','P','Q']
    queryString = ((model['tick'].str.len() <= 4) | (model['tick'].str.len() > 4) & (~model['tick'].str[-1:].isin(terminating_symbol) ) )     
    return model.loc[queryString]
    

def getModelFromFile(model):
    if model == 'nasdaq':    
        df_nasdaq = pd.read_csv('nasdaq_nasdaq.csv')
        df_all = df_nasdaq
        del df_nasdaq

        df = pd.DataFrame()
        df['tick'] = df_all['Symbol']
        df['name'] = df_all['Name']
        df['market_cap'] = df_all['Market Cap']
        df['volume'] = df_all['Volume']
        df['ipo_year'] = df_all['IPO Year']
        df['sector'] = df_all['Sector']
        df['industry'] = df_all['Industry']
        df['country'] = df_all['Country']
        
        # print(df.isna().any())
        df['market_cap'] = df['market_cap'].fillna(0)
        df['ipo_year'] = df['ipo_year'].fillna('0')
        df['sector'] = df['sector'].fillna('')
        df['industry'] = df['industry'].fillna('')
        df['country'] = df['country'].fillna('')
        # print(df.isna().any())

        return df
    elif model == 'nyse':    
        df_nyse = pd.read_csv('nasdaq_nyse.csv')
        df_all = df_nyse 
        del df_nyse

        df = pd.DataFrame()
        df['tick'] = df_all['Symbol']
        df['name'] = df_all['Name']
        df['market_cap'] = df_all['Market Cap']
        df['volume'] = df_all['Volume']
        df['ipo_year'] = df_all['IPO Year']
        df['sector'] = df_all['Sector']
        df['industry'] = df_all['Industry']
        df['country'] = df_all['Country']
        
        # print(df.isna().any())
        df['market_cap'] = df['market_cap'].fillna(0)
        df['ipo_year'] = df['ipo_year'].fillna('0')
        df['sector'] = df['sector'].fillna('')
        df['industry'] = df['industry'].fillna('')
        df['country'] = df['country'].fillna('')
        # print(df.isna().any())

        return df
    else:        
        df_nasdaq = pd.read_csv('nasdaq_nasdaq.csv')
        df_nyse = pd.read_csv('nasdaq_nyse.csv')
        df_all = pd.concat([df_nasdaq, df_nyse], ignore_index=True)
        del df_nasdaq, df_nyse

        df = pd.DataFrame()
        df['tick'] = df_all['Symbol']
        df['name'] = df_all['Name']
        df['market_cap'] = df_all['Market Cap']
        df['volume'] = df_all['Volume']
        df['ipo_year'] = df_all['IPO Year']
        df['sector'] = df_all['Sector']
        df['industry'] = df_all['Industry']
        df['country'] = df_all['Country']
        
        # print(df.isna().any())
        df['market_cap'] = df['market_cap'].fillna(0)
        df['ipo_year'] = df['ipo_year'].fillna('0')
        df['sector'] = df['sector'].fillna('')
        df['industry'] = df['industry'].fillna('')
        df['country'] = df['country'].fillna('')
        # print(df.isna().any())

        return df