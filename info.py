import requests 
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from re import sub
from decimal import Decimal
import json
import yfinance as yf
from bs4 import BeautifulSoup
import requests


def fetchInfo(ticker):
    
    headers = {
        'authority': 'api.nasdaq.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,th;q=0.8',
        'origin': 'https://www.nasdaq.com',
        'referer': 'https://www.nasdaq.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }

    params = {
        'assetclass': 'stocks',
    }

    try:
        response = requests.get('https://api.nasdaq.com/api/quote/' + ticker + '/info', params=params, headers=headers)        
        response_json = response.json()        
        info = response_json['data']
        

        #print(response_json_data.keys())
        #print(response_json_data['dividends'].keys())
        #print(response_json_data['dividends']['headers'])
        # print(response_json_data['dividends']['rows'])
        
        if info is not None and response_json['status']['rCode'] == 200:        
            return info
        else:
            return []
    except TypeError:
        return []

def fetchDetail(ticker):
    headers = {
        'authority': 'api.nasdaq.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,th;q=0.8',
        'origin': 'https://www.nasdaq.com',
        'referer': 'https://www.nasdaq.com/',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }

    params = {
        'assetclass': 'stocks',
    }

    
    try:
        response = requests.get('https://api.nasdaq.com/api/quote/' + ticker + '/summary', params=params, headers=headers)
        
        response_json = response.json()        
        info = response_json['data']
        

        #print(response_json_data.keys())
        #print(response_json_data['dividends'].keys())
        #print(response_json_data['dividends']['headers'])
        # print(response_json_data['dividends']['rows'])
        
        if info is not None and response_json['status']['rCode'] == 200:        
            return info
        else:
            return []
    except TypeError:
        return []

def load(model):
    # return pd.read_csv('dividends.csv')    
    return pd.read_csv(model)        



def model(dividend_df): 
    name = []
    stock_type = []
    exchange = []
    industry = []
    sector = [] 
    share_volume = []
    trade_volume = []
    market_cap = []
    low_today = []
    high_today = []
    low_52 = []
    high_52 = []
    previous_close = []
    _pe = []
    _yield = []
    _eps = []
    _annualized_dividend = []
    

    _price_zone = [] # (last - low_52) / (high_52 - low_52)
    _dpr = [] # 
    _highest_yield = [] # low_52_dividend / low_52
    _target_price = [] # _yield / _highest_yield
    _zone1 = [] # _yield / (_highest_yield * 90%)
    _zone2 = [] # _yield / (_highest_yield * 80%)
    _money_trail = [] # 'good' if last - zone1 < 0; 'ok' if (last - zone1 > 0) and (last - zone2 < 0); otherwise 'bad'
    _price_trail = [] # 'good' if _price_zone < 40%; 'ok' if (_price_zone > 40%) and (_price_zone < 60%); otherwise 'bad'
    
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            "(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        }

    for index, row in dividend_df.iterrows():
        print(row['tick'])  

        data = fetchDetail(row['tick'])

        #obj = yf.Ticker(row['tick'])
        html = requests.get('https://finance.yahoo.com/quote/' + row['tick'] + '?p=' + row['tick'] , headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')


        #if len(data) and data['summaryData']['ShareVolume']['value'] != 'N/A' and data['summaryData']['AverageVolume']['value'] != 'N/A' and data['summaryData']['MarketCap']['value'] != 'N/A' :
        if len(data):
            exchange.append(data['summaryData']['Exchange']['value'])
            industry.append(data['summaryData']['Sector']['value'])
            sector.append(data['summaryData']['Industry']['value'])    

            #float(Decimal(sub(r'[^\d.]', '', highlow_52[0])))
            #share_volume.append(int((data['summaryData']['ShareVolume']['value']).replace(",","")))                

            share_volume.append(data['summaryData']['ShareVolume']['value'])
            trade_volume.append(data['summaryData']['AverageVolume']['value'])

            #market_cap.append(data['summaryData']['MarketCap']['value'])
            #market_cap.append(str(obj.info['marketCap']))
            mc = '0'
            for item in soup.find_all('td'):
                if "data-test" in item.attrs:
                    if item["data-test"] == "MARKET_CAP-value":    
                        if item.text != 'N/A':                    
                            if item.text[-1] == 'M' or item.text[-1] == 'm':
                                mc = str(float(item.text[:-1]) * 1000000)
                            elif item.text[-1] == 'B' or item.text[-1] == 'b':
                                mc = str(float(item.text[:-1]) * 1000000000)
                            elif item.text[-1] == 'T' or item.text[-1] == 't':
                                mc = str(float(item.text[:-1]) * 1000000000000)
                            elif item.text[-1] == 'Q' or item.text[-1] == 'q':
                                mc = str(float(item.text[:-1]) * 1000000000000000)
                        else:
                            mc = str(item.text)

                        break  
            print('market cap: ', mc)
            market_cap.append(mc)  

            highlow_today = data['summaryData']['TodayHighLow']['value'].split("/")        
            highlow_52 = data['summaryData']['FiftTwoWeekHighLow']['value'].split("/")  

            low_today.append(highlow_today[0])
            high_today.append(highlow_today[1])
            low_52.append(highlow_52[0])
            high_52.append(highlow_52[1])
            previous_close.append(data['summaryData']['PreviousClose']['value'])        
            _pe.append(str(data['summaryData']['PERatio']['value']))
            _yield.append(data['summaryData']['Yield']['value'])
            _eps.append(data['summaryData']['EarningsPerShare']['value'])                       
            _annualized_dividend.append(data['summaryData']['AnnualizedDividend']['value'])
        else:
            exchange.append("")
            industry.append("")
            sector.append("")        

            share_volume.append('0')
            trade_volume.append('0')
            market_cap.append('0')
            
            low_today.append('0.0')
            high_today.append('0.0')
            low_52.append('0.0')
            high_52.append('0.0')

            previous_close.append('0.0')
            _pe.append('0.0')
            _yield.append('0.0')
            _eps.append('0.0')
            _annualized_dividend.append('0.0')

        

    dividend_df['exchange'] = exchange
    dividend_df['exchange'] = dividend_df['exchange'].fillna('')
    dividend_df['exchange'] = dividend_df['exchange'].str.replace('N/A','')

    dividend_df['industry'] = industry
    dividend_df['industry'] = dividend_df['industry'].fillna('')
    dividend_df['industry'] = dividend_df['industry'].str.replace('N/A','')

    dividend_df['sector'] = sector
    dividend_df['sector'] = dividend_df['sector'].fillna('')
    dividend_df['sector'] = dividend_df['sector'].str.replace('N/A','')

    dividend_df['share_volume'] = share_volume
    dividend_df['share_volume'] = dividend_df['share_volume'].fillna('0.0')
    dividend_df['share_volume'] = dividend_df['share_volume'].str.replace('N/A','0.0')
    dividend_df['share_volume'] = dividend_df['share_volume'].str.replace('$','')
    dividend_df['share_volume'] = dividend_df['share_volume'].str.replace(',','')
    dividend_df['share_volume'] = dividend_df['share_volume'].astype(float)


    dividend_df['trade_volume'] = trade_volume
    dividend_df['trade_volume'] = dividend_df['trade_volume'].fillna('0.0')
    dividend_df['trade_volume'] = dividend_df['trade_volume'].str.replace('N/A','0.0')
    dividend_df['trade_volume'] = dividend_df['trade_volume'].str.replace('$','')
    dividend_df['trade_volume'] = dividend_df['trade_volume'].str.replace(',','')
    dividend_df['trade_volume'] = dividend_df['trade_volume'].astype(float)


    dividend_df['market_cap'] = market_cap
    dividend_df['market_cap'] = dividend_df['market_cap'].fillna('0')
    dividend_df['market_cap'] = dividend_df['market_cap'].str.replace('N/A','0')
    # dividend_df['market_cap'] = dividend_df['market_cap'].str.replace('M','000000')
    # dividend_df['market_cap'] = dividend_df['market_cap'].str.replace('b','000000000')
    # dividend_df['market_cap'] = dividend_df['market_cap'].str.replace('B','000000000')
    # dividend_df['market_cap'] = dividend_df['market_cap'].str.replace('T','000000000000')
    # dividend_df['market_cap'] = dividend_df['market_cap'].str.replace('t','000000000000')
    # dividend_df['market_cap'] = dividend_df['market_cap'].str.replace('$','')
    dividend_df['market_cap'] = dividend_df['market_cap'].str.replace(',','')
    dividend_df['market_cap'] = dividend_df['market_cap'].astype(float)


    dividend_df['low_today'] = low_today
    dividend_df['low_today'] = dividend_df['low_today'].fillna('0')
    dividend_df['low_today'] = dividend_df['low_today'].str.replace('A','0')
    dividend_df['low_today'] = dividend_df['low_today'].str.replace('N','0')
    dividend_df['low_today'] = dividend_df['low_today'].str.replace('N/A','0')
    dividend_df['low_today'] = dividend_df['low_today'].str.replace('$','')
    dividend_df['low_today'] = dividend_df['low_today'].str.replace(',','')
    dividend_df['low_today'] = dividend_df['low_today'].astype(float)

    dividend_df['high_today'] = high_today
    dividend_df['high_today'] = dividend_df['high_today'].fillna('0')
    dividend_df['high_today'] = dividend_df['high_today'].str.replace('A','0')
    dividend_df['high_today'] = dividend_df['high_today'].str.replace('N','0')
    dividend_df['high_today'] = dividend_df['high_today'].str.replace('N/A','0')
    dividend_df['high_today'] = dividend_df['high_today'].str.replace('$','')
    dividend_df['high_today'] = dividend_df['high_today'].str.replace(',','')
    dividend_df['high_today'] = dividend_df['high_today'].astype(float)

    dividend_df['low_52'] = low_52
    dividend_df['low_52'] = dividend_df['low_52'].fillna('0')
    dividend_df['low_52'] = dividend_df['low_52'].str.replace('A','0')
    dividend_df['low_52'] = dividend_df['low_52'].str.replace('N','0')
    dividend_df['low_52'] = dividend_df['low_52'].str.replace('N/A','0')
    dividend_df['low_52'] = dividend_df['low_52'].str.replace('$','')
    dividend_df['low_52'] = dividend_df['low_52'].str.replace(',','')
    dividend_df['low_52'] = dividend_df['low_52'].astype(float)


    dividend_df['high_52'] = high_52
    dividend_df['high_52'] = dividend_df['high_52'].fillna('0')
    dividend_df['high_52'] = dividend_df['high_52'].str.replace('A','0')
    dividend_df['high_52'] = dividend_df['high_52'].str.replace('N','0')
    dividend_df['high_52'] = dividend_df['high_52'].str.replace('N/A','0')
    dividend_df['high_52'] = dividend_df['high_52'].str.replace('$','')
    dividend_df['high_52'] = dividend_df['high_52'].str.replace(',','')
    dividend_df['high_52'] = dividend_df['high_52'].astype(float)

    dividend_df['previous_close'] = previous_close
    dividend_df['previous_close'] = dividend_df['previous_close'].fillna('0')
    dividend_df['previous_close'] = dividend_df['previous_close'].str.replace('A','0')
    dividend_df['previous_close'] = dividend_df['previous_close'].str.replace('N','0')
    dividend_df['previous_close'] = dividend_df['previous_close'].str.replace('N/A','0')
    dividend_df['previous_close'] = dividend_df['previous_close'].str.replace('$','')
    dividend_df['previous_close'] = dividend_df['previous_close'].str.replace(',','')
    dividend_df['previous_close'] = dividend_df['previous_close'].astype(float)

    dividend_df['_pe'] = _pe
    dividend_df['_pe'] = dividend_df['_pe'].fillna('0')
    dividend_df['_pe'] = dividend_df['_pe'].str.replace('N/A','0')
    dividend_df['_pe'] = dividend_df['_pe'].str.replace('$','')
    dividend_df['_pe'] = dividend_df['_pe'].str.replace(',','')
    dividend_df['_pe'] = dividend_df['_pe'].astype(float)


    dividend_df['_yield'] = _yield 
    dividend_df['_yield'] = dividend_df['_yield'].fillna('0.0')
    dividend_df['_yield'] = dividend_df['_yield'].str.replace('N/A','0.0')
    dividend_df['_yield'] = dividend_df['_yield'].str.replace('$','')
    dividend_df['_yield'] = dividend_df['_yield'].str.replace('%','')
    dividend_df['_yield'] = dividend_df['_yield'].str.replace(',','')
    dividend_df['_yield'] = dividend_df['_yield'].astype(float)


    dividend_df['_eps'] = _eps
    dividend_df['_eps'] = dividend_df['_eps'].fillna('0.0')
    dividend_df['_eps'] = dividend_df['_eps'].str.replace('N/A','0.0')
    dividend_df['_eps'] = dividend_df['_eps'].str.replace('$','')
    dividend_df['_eps'] = dividend_df['_eps'].str.replace(',','')
    dividend_df['_eps'] = dividend_df['_eps'].astype(float)


    dividend_df['_annualized_dividend'] = _annualized_dividend
    dividend_df['_annualized_dividend'] = dividend_df['_annualized_dividend'].fillna('0.0')
    dividend_df['_annualized_dividend'] = dividend_df['_annualized_dividend'].str.replace('N/A','0.0')
    dividend_df['_annualized_dividend'] = dividend_df['_annualized_dividend'].str.replace('$','')
    dividend_df['_annualized_dividend'] = dividend_df['_annualized_dividend'].str.replace(',','')
    dividend_df['_annualized_dividend'] = dividend_df['_annualized_dividend'].astype(float)

    return dividend_df

def save(df, model):
    df.to_csv(model)






