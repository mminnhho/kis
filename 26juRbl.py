"""
Ticker: TQQQ, TMF
Threshold: 1 to 10 percent
Amount: 10 ~ 90 percent
Price: Open, Close
Fee: 0.07 percent
"""

import pandas as pd

dfQ = pd.read_csv("TQQQ.csv")
dfM = pd.read_csv("TMF.csv")

threshold= [(1/100) * x for x in range(3,4)]
amount = [(1/100) * x for x in range(10,11)]
fee = 0.0007

capital = 10000

#print(dfQ.head(7))
#print(dfM.head(7))

for t in threshold:
    for a in amount:
        srQ = dfQ.iloc[0]
        tPriceQ = srQ[4]
        srM = dfM.iloc[0]
        tPriceM = srM[4]

        if tPriceQ > tPriceM:
            stkQ = int((capital/2) / tPriceQ)
            stkM = int((capital-tPriceQ*stkQ) / tPriceM)
            cash = capital - tPriceQ*stkQ - tPriceM*stkM
        else:
            stkM = int((capital/2) / tPriceM)
            stkQ = int((capital-tPriceM*stkM) / tPriceQ)
            cash = capital - tPriceQ*stkQ - tPriceM*stkM
        print(stkQ, stkM, cash)

#        for i in range(1,len(dfQ)):
        for i in range(1,50):
            for p in ['Open','Close']:
                srQ = dfQ.iloc[i]
                priceQ = srQ[p]
                date = srQ[0]
                srM = dfM.iloc[i]
                priceM = srM[p]
                gap = abs(priceQ/tPriceQ - priceM/tPriceM)
                if gap > t:
                    print('date', date, 'priceQ', priceQ, 'priceM', priceM, 'gap', gap)
                    tPriceQ = priceQ
                    tPriceM = priceM

