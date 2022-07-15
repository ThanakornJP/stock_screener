import xxlimited
from numpy import inner
import requests 
from bs4 import BeautifulSoup
import pandas as pd

def getHeader(source):    
    if source == 'nasdaq':
        return {
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
    elif source == 'yahoo':
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            "(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        }
    
def fetchSummaryFromNasdaq(tick):
    headers = getHeader('nasdaq')
    params = { 'assetclass': 'stocks'}
    try:
        response = requests.get('https://api.nasdaq.com/api/quote/' + tick + '/summary', params=params, headers=headers)
        
        response_json = response.json()     
        info = response_json['data']['summaryData']
        
        if info is not None and response_json['status']['rCode'] == 200:        
            return info
        else:
            return None
    except TypeError:
        return None

def fetchSummaryFromYahoo(source, tick):
    headers = getHeader('yahoo')
    params = { 'assetclass': 'stocks'}
    try:
        response = requests.get('https://api.nasdaq.com/api/quote/' + tick + '/summary', params=params, headers=headers)
        
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

def fetchDividendFromNasdaq(tick):
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
        response = requests.get('https://api.nasdaq.com/api/quote/' + tick + '/dividends', params=params, headers=headers)
        response_json = response.json()        
        response_json_data = response_json['data']        
        dividends = response_json_data['dividends']['rows']
        if dividends is not None:        
            return dividends
        else:
            return None
    except TypeError:
        return None


def fetch5YFromAlphaVantage(tick):

    try:
        # html = requests.get('https://finance.yahoo.com/quote/' + row['tick'] + '?p=' + row['tick'] , headers=headers)
        # soup = BeautifulSoup(html.text, 'lxml')
        # requests.get('https://eodhistoricaldata.com/api/eod/AAPL.US?api_token=demo&from=2016-01-01&to=2021-12-31')        
        # response_json = response.json()        
        # info = response_json['data']
        
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + tick + '&outputsize=full&apikey=HXXBQ51QZIU5O0QH'
        r = requests.get(url)
        data = r.json()

        if data is not None:        
            return data
        else:
            return []
    except TypeError:
        return []


def fetch5YFromBarchart(tick):
    info = {}
    try:        
        url = 'https://www.barchart.com/stocks/quotes/' + tick + '/performance?mode=daily'
        print(url)
        html = requests.get(url, headers=getHeader('yahoo'))
        soup = BeautifulSoup(html.text, 'lxml')
        a = soup.find("div",{"class":"barchart-content-block symbol-price-performance"})
        # print(len(a.contents))
        # print(list(a.contents[3].contents[1].contents[1].children))
        # print(len(list(a.contents[3].contents[1].contents[1].children)))
        # print(list(a.contents[3].contents[1].contents[1].children)[19])
        # print(list(list(a.contents[3].contents[1].contents[1].children)[19]))


        # 0-2: header
        # 3: 5 day
        # 5: 1 month
        # 7: 3 month
        # 9: 6 month 
        # 11: YTD
        # 13: 52wk 
        # 15: 2Y
        # 17: 3y
        # 19: 5y
        # 21: 10y
        # 23: 20y

        if len(list(a.contents[3].contents[1].contents[1].children)) >= 20:    
            info['low_5y'] = list(list(a.contents[3].contents[1].contents[1].children)[19])[3].find_all('span')[0].getText()
            info['high_5y'] = list(list(a.contents[3].contents[1].contents[1].children)[19])[7].find_all('span')[0].getText()
            info['open_5y'] = list(list(a.contents[3].contents[1].contents[1].children)[19])[5].find('barchart-row-chart')['data-open-price']
            info['last_in_5y'] = list(list(a.contents[3].contents[1].contents[1].children)[19])[5].find('barchart-row-chart')['data-approach']
            info['change_5y'] = list(list(a.contents[3].contents[1].contents[1].children)[19])[9].find_all('span')[0].getText()
            info['change%_5y'] = list(list(a.contents[3].contents[1].contents[1].children)[19])[9].find_all('span')[1].getText()
        else:
            info['low_5y'] = '0'
            info['high_5y'] = '0'
            info['open_5y'] = '0'
            info['last_in_5y'] = '0'
            info['change_5y'] = '0'
            info['change%_5y'] = '0'

        print(info)

        if len(info) > 0:        
            return info
        else:
            return []
    except TypeError:
        return []