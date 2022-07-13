import pandas as pd

def attribute_data(model):
    raw_dividends = []

    for index, row in model.iterrows():     
        print(row['tick'])           
        info = src.fetchDividendFromNasdaq(row['tick'])

        # print(row['tick'], ' ==> ')
        # print(info)
        if info is None:
            raw_dividends.append([])           
        else: 
            raw_dividends.append(info)
            
    model['raw_dividends'] = raw_dividends
    return model