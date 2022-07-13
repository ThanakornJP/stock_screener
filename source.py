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


def fetchEarningFromYahoo(tick):
    headers = getHeader('yahoo')
    try:
        html = requests.get('https://finance.yahoo.com/quote/' + row['tick'] + '?p=' + row['tick'] , headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')

        # for item in soup.find_all('td'):
        #         if "data-test" in item.attrs:
        #             if item["data-test"] == "MARKET_CAP-value": 

        if info is not None and response_json['status']['rCode'] == 200:        
            return info
        else:
            return []
    except TypeError:
        return []