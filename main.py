
from random import triangular
from tempfile import TemporaryFile
import pandas as pd
import re

import ticker as tk
import info as i
import dividend as dvd
import source as src


def initModel(mode):
    if mode == 'new':
        model = tk.getModelFromFile('all')
        model = tk.filterOut(model) #exclude terminating stocks
        tk.saveToFile(model + 'model.csv')
        return model
    else:
        return pd.read_csv('model.csv') # read existing model

def getQueryByMarketCap(sizing, model):
    if sizing == 'all': return model['market_cap'] > 0  # all 
    elif sizing == 'xl': return model['market_cap'] > 200000000000  # Mega Cap > 200B
    elif sizing == 'l': return (model['market_cap'] > 10000000000) & (model['market_cap'] <= 200000000000) # 10B < Large Cap <= 200B
    elif sizing == 'm': return (model['market_cap'] > 2000000000) & (model['market_cap'] <= 10000000000) # 2B < Medium Cap <= 10B
    elif sizing == 's': return (model['market_cap'] > 300000000) & (model['market_cap'] <= 2000000000) # 300M < Small Cap <= 2B
    elif sizing == 'xs': return model['market_cap'] <= 300000000 #  Micro Cap <= 300M
    else: return model['market_cap'] <= 300000000 #  Micro Cap <= 300M


# read - no update at all
# reload - update all
# refresh - update attribution
def loadModel(mode, sizing):
    if mode == "read":
        return pd.read_csv('model.attributed.' + sizing + '.csv')
    else:
        model = pd.DataFrame()
        if mode == 'reload':
            model = initModel('new') 
        elif mode == 'refresh':
            model = initModel(None)
        
        queryString = getQueryByMarketCap(sizing, model)
        filtered_model = model.loc[queryString]
        print('# selected rows (' + sizing + '): ', len(filtered_model.index))
        print('sample rows')
        print(filtered_model.head())
        print(filtered_model.tail())

        filtered_model = i.attribute_data(filtered_model)
        filtered_model = i.clean_stat(filtered_model)
        filtered_model = i.clean_ratio(filtered_model)
        print('sample rows after getting attributed')
        print(filtered_model.head())
        print(filtered_model.tail())

        filtered_model = dvd.attribute_data(filtered_model)
        filtered_model = dvd.attribute_recession_proof(filtered_model)
        filtered_model = dvd.attribute_streak(filtered_model)

        filtered_model.to_csv('model.attributed.' + sizing + '.csv')
        return filtered_model

def loadShortList():
    modelM = loadModel("read", "m")
    modelL = loadModel("read", "l")
    modelXL = loadModel("read", "xl")

    model = pd.concat([modelM, modelL, modelXL], ignore_index=True)
     
    print(model.info())

    queryString = "industry != '' " \
        "and sector != '' " \
        "and num_streak > 3.9 " \
        "and num_surviving_years_since_ipo > 6.3 " \
        "and market_cap > 2.75e+10"
        
    df = model.query(queryString).sort_values(by=['market_cap', 'num_streak', 'volume'], ascending=False)
    # print(df['num_streak'].describe()) #std 13.3, mean 3.9 
    # print(df['num_surviving_years_thru_recession'].describe()) #std 0.86, mean 1.24
    # print(df['num_surviving_years_since_ipo'].describe()) #std 7.1, mean 6.3
    # print(df['market_cap'].describe()) #  std 1.05e+11, mean 2.75e+10

    print('# selected rows: ', len(df.index))
    print(df)
    df.to_csv('model.attributed.shortlist.csv')


#model = pd.read_csv('model.attributed.shortlist.csv')

src.fetchEarningFromYahoo('AAPL')

