
import pandas as pd
import re

import ticker as tk
import info as i
import dividend as dvd


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
        filtered_model.to_csv('model.attributed.' + sizing + '.csv')
        return filtered_model
    


# 1. load model
model = loadModel("read", "m")

queryString = "industry == '' " \
    "or sector == '' " \
    "or market_cap <= 0 " \

df = model.query(queryString).sort_values(by=['market_cap'], ascending=False)
print('# selected rows: ', len(df.index))


# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------

# print(dividend_with_info.query(queryString)[['tick','num_streak', 'market_cap','industry','sector']].sort_values(by=['market_cap'] , ascending=False))



# dvd.reload()
# i.save(i.model(pd.read_csv('dividends.nasdaq.csv')),'dividends_with_info.nasdaq.csv')
# dividend_with_info = i.getModel()


# print(dividend_with_info.info())
# #print(dividend_with_info.head())
# print(dividend_with_info.isna().any())
# #print(dividend_with_info.isnull().any())

# print(dividend_with_info[dividend_with_info['exchange'].isna()])
# print(dividend_with_info[dividend_with_info['industry'].notna()])
# print(dividend_with_info[dividend_with_info['sector'].isna()])
# print(dividend_with_info[dividend_with_info['share_volume'].isna()])
# print(dividend_with_info[dividend_with_info['trade_volume'].isna()])
# print(dividend_with_info[dividend_with_info['market_cap'].isna()])
# print(dividend_with_info[dividend_with_info['_pe'].isna()])
# print(dividend_with_info[dividend_with_info['_yield'].isna()])
# print(dividend_with_info[dividend_with_info['_annualized_dividend'].isna()])
# print(dividend_with_info[dividend_with_info['_eps'].isna()])
# print(dividend_with_info[dividend_with_info['_eps'].isnull()])

#print(dividend_with_info[dividend_with_info.isna().any(axis=1)])
#print(dividend_with_info[dividend_with_info.isnull().any(axis=1)])


#dividend_with_info['_eps'] = dividend_with_info['_eps'].fillna(0)

#print(dividend_with_info[dividend_with_info['industry'].isna()])

#float(Decimal(sub(r'[^\d.]', '', highlow_52[0])))
#share_volume.append(int((data['summaryData']['ShareVolume']['value']).replace(",","")))                

# dividend_with_info['exchange'] = dividend_with_info['exchange'].fillna('')
# dividend_with_info['industry'] = dividend_with_info['industry'].fillna('')
# dividend_with_info['sector'] = dividend_with_info['sector'].fillna('')

# dividend_with_info['share_volume'] = dividend_with_info['share_volume'].fillna('0.0')
# dividend_with_info['share_volume'] = dividend_with_info['share_volume'].str.replace('$','')
# dividend_with_info['share_volume'] = dividend_with_info['share_volume'].str.replace(',','')
# dividend_with_info['share_volume'] = dividend_with_info['share_volume'].astype(float)

# dividend_with_info['trade_volume'] = dividend_with_info['trade_volume'].fillna('0.0')
# dividend_with_info['trade_volume'] = dividend_with_info['trade_volume'].str.replace('$','')
# dividend_with_info['trade_volume'] = dividend_with_info['trade_volume'].str.replace(',','')
# dividend_with_info['trade_volume'] = dividend_with_info['trade_volume'].astype(float)

# dividend_with_info['market_cap'] = dividend_with_info['market_cap'].fillna('0.0')
# dividend_with_info['market_cap'] = dividend_with_info['market_cap'].str.replace('$','')
# dividend_with_info['market_cap'] = dividend_with_info['market_cap'].str.replace(',','')
# dividend_with_info['market_cap'] = dividend_with_info['market_cap'].astype(float)

# dividend_with_info['_pe'] = dividend_with_info['_pe'].fillna('0.0')
# dividend_with_info['_pe'] = dividend_with_info['_pe'].str.replace('$','')
# dividend_with_info['_pe'] = dividend_with_info['_pe'].str.replace(',','')
# dividend_with_info['_pe'] = dividend_with_info['_pe'].astype(float)

# dividend_with_info['_yield'] = dividend_with_info['_yield'].fillna('0.0')
# dividend_with_info['_yield'] = dividend_with_info['_yield'].str.replace('$','')
# dividend_with_info['_yield'] = dividend_with_info['_yield'].str.replace('%','')
# dividend_with_info['_yield'] = dividend_with_info['_yield'].str.replace(',','')
# dividend_with_info['_yield'] = dividend_with_info['_yield'].astype(float)

# dividend_with_info['_eps'] = dividend_with_info['_eps'].fillna('0.0')
# dividend_with_info['_eps'] = dividend_with_info['_eps'].str.replace('$','')
# dividend_with_info['_eps'] = dividend_with_info['_eps'].str.replace(',','')
# dividend_with_info['_eps'] = dividend_with_info['_eps'].astype(float)


# dividend_with_info['_annualized_dividend'] = dividend_with_info['_annualized_dividend'].fillna('0.0')
# dividend_with_info['_annualized_dividend'] = dividend_with_info['_annualized_dividend'].str.replace('$','')
# dividend_with_info['_annualized_dividend'] = dividend_with_info['_annualized_dividend'].str.replace(',','')
# dividend_with_info['_annualized_dividend'] = dividend_with_info['_annualized_dividend'].astype(float)


# print(dividend_with_info.info())

# queryString = "exchange != '' " \
#     "and industry != '' " \
#     "and sector != '' " \
#     "and share_volume > 0.0 " \
#     "and trade_volume > 0.0 " \
#     "and market_cap > 0.0 " \
#     "and _pe > 0.0 " \
#     "and _yield > 0.0 " \
#     "and _eps > 0.0 " \
#     "and _annualized_dividend > 0.0 "


# work!
# queryString = "exchange != '' " \
#     "and industry != '' " \
#     "and sector != '' " \
#     "and market_cap > 1000000 " \
#     "and _pe > 0"

# print(dividend_with_info.query(queryString)[['tick','num_streak', 'market_cap','industry','sector']].sort_values(by=['market_cap'] , ascending=False))
