"""
Ticker: TQQQ, TMF
Threshold: 1 to 10 percent
AmountRate: 10 ~ 90 percent
Price: Open, Close
FeeRate: 0.07 percent
==> Rebalance twice a day!
"""

import pandas as pd

dfQ = pd.read_csv("TQQQ.csv")
dfM = pd.read_csv("TMF.csv")

#threshold= [(1/100) * x for x in range(1,31)]
amountRate = [(1/100) * x for x in range(1,91)]
feeRate = 0.0007

capital = 10000
balMax = 0
tMax = 0
arMax = 0

for a in amountRate:
    srQ = dfQ.iloc[0]
    tPriceQ = srQ[4]
    srM = dfM.iloc[0]
    tPriceM = srM[4]

    taMax = 0

    if tPriceQ > tPriceM:
        stkQ = int((capital/2) / tPriceQ)
        stkM = int((capital-tPriceQ*stkQ) / tPriceM)
        cash = capital - tPriceQ*stkQ - tPriceM*stkM
    else:
        stkM = int((capital/2) / tPriceM)
        stkQ = int((capital-tPriceM*stkM) / tPriceQ)
        cash = capital - tPriceQ*stkQ - tPriceM*stkM
#        print(stkQ, stkM, cash)

    for i in range(1,len(dfQ)):
#        for i in range(1,50):
        for p in ['Open','Close']:
            srQ = dfQ.iloc[i]
            priceQ = srQ[p]
            date = srQ[0]
            srM = dfM.iloc[i]
            priceM = srM[p]

            gap = abs(priceQ/tPriceQ - priceM/tPriceM)

            if priceQ/tPriceQ > priceM/tPriceM:
                amountQ = int(stkQ * a)
                stkQ -= amountQ
                cash += (priceQ * amountQ) * (1 - feeRate)
                amountM = int(cash / (1 + feeRate) / priceM)
                stkM += amountM
                cash -= (priceM * amountM) * (1 + feeRate)
                bal = priceQ*stkQ + priceM*stkM + cash

            if priceM/tPriceM > priceQ/tPriceQ:
                amountM = int(stkM * a)
                stkM -= amountM
                cash += (priceM * amountM) * (1 - feeRate)
                amountQ = int(cash / (1 + feeRate) / priceQ)
                stkQ += amountQ
                cash -= (priceQ * amountQ) * (1 + feeRate)
                bal = priceQ*stkQ + priceM*stkM + cash

            if bal > balMax:
                balMax = bal
                arMax = a

            tPriceQ = priceQ
            tPriceM = priceM

#                    print('date', date, 'priceQ', priceQ, 'priceM', priceM, 'gap', gap, 'stkQ', stkQ, 'stkM', stkM, 'cash', cash, 'bal', bal)

print('balMax', balMax, 'arMax', arMax)
