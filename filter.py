import source as src 

def filterByMoneyTrail(model):
    money_trail = []
    for index, row in model.iterrows():
        
        if float(row['last']) <= float(row['zone_1']):
            money_trail.append('good')
        elif float(row['last']) > float(row['zone_1']) and float(row['last']) <= float(row['zone_2']):
            money_trail.append('ok')
        else:
            money_trail.append('bad')
    model['money_trail'] = money_trail
    return model



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



def filterByPriceTrail(model):
    priceTrail = []
    for index, row in model.iterrows():
        if row['price_zone'] <= 0.40:
            priceTrail.append('good')
        elif row['price_zone'] > 0.40 and row['price_zone'] <= 0.60:
            priceTrail.append('ok')
        else:
            priceTrail.append('bad')
    
    model['priace_trail'] = priceTrail
    return model
    