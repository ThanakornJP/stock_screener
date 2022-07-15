import xxlimited
import source as src 

def getTargetPrice(model):
    ##highest_dividend_yield = model.5y_low_dividend / model.5y_low
    return model.current_dividend / highest_dividend_yield

def getLatestPrice(tick):
    return src.getLatestPrice(tick)

def filterByGrade(model):
    if model.dpr > 50 and model.dpr <= 70:
        return 'AAA'
    elif model.dpr > 30 and model.dpr <= 50:
        return 'AA'
    else:   
        return 'A'
    # Grade AAA: consecutive payout 25Y+, DPR 50-70%, growth (leap probability) lowest
    # Grade AA: consecutive payout 10-20Y+, DPR 30-50%
    # Grade A: consecutive payout 5-10Y+, DPR 10-30%, growth (leap probability) highest
    return 

def filterByMoneyTrail(model):


    for index, row in model.iterrows():
        xxlimited

        #highest_dividend_yield = model.5y_low_dividend / row['5y_low']
        zone_1st = model.current_dividend / (highest_dividend_yield * 0.9)
        zone_2nd = model.current_dividend / (highest_dividend_yield * 0.8)


    if model.last <= zone_1st:
        return 'good'
    elif model.last > zone_1st and model.last <= zone_2nd:
        return 'ok'
    else:
        return 'bad'

def filterByPriceTrail(model):
    priceTrail = []
    for index, row in model.iterrows():
        price_zone = ( getLatestPrice(row['tick']) - row['low_52'] ) / (row['high_52'] - row['low_52'])
        if price_zone <= 40:
            priceTrail.append('good')
        elif price_zone > 40 and price_zone <= 60:
            priceTrail.append('ok')
        else:
            priceTrail.append('bad')
    
    model['priace_trail'] = priceTrail
    return model
    