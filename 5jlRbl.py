"""
Ticker: TQQQ, TMF
Threshold: 1 to 10 percent
AmountRate: 10 ~ 90 percent
=> Price: Open
FeeRate: 0.07 percent
=> Rebalance at Threshold!
"""

import pandas as pd

dfQ = pd.read_csv("TQQQ.csv")
dfM = pd.read_csv("UGL.csv")

threshold= [(1/100) * x for x in range(1,101)]
amountRate = [(1/100) * x for x in range(1,101)]
feeRate = 0.0007

capital = 10000
balMax = 0
tMax = 0
arMax = 0

dfO = pd.DataFrame(columns = ['t', 'a', 'bal'])

for t in threshold:
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
            for p in ['Open']:
#            for p in ['Open', 'Close']:
                srQ = dfQ.iloc[i]
                priceQ = srQ[p]
                date = srQ[0]
                srM = dfM.iloc[i]
                priceM = srM[p]

                gap = abs(priceQ/tPriceQ - priceM/tPriceM)
                if gap > t:
                    if priceQ/tPriceQ > priceM/tPriceM:
                        amountQ = int(stkQ * a)
                        stkQ -= amountQ
                        cash += (priceQ * amountQ) * (1 - feeRate)
                        amountM = int(cash / (1 + feeRate) / priceM)
                        stkM += amountM
                        cash -= (priceM * amountM) * (1 + feeRate)

                    if priceM/tPriceM > priceQ/tPriceQ:
                        amountM = int(stkM * a)
                        stkM -= amountM
                        cash += (priceM * amountM) * (1 - feeRate)
                        amountQ = int(cash / (1 + feeRate) / priceQ)
                        stkQ += amountQ
                        cash -= (priceQ * amountQ) * (1 + feeRate)

                    tPriceQ = priceQ
                    tPriceM = priceM

                    if len(threshold)==1 and len(amountRate)==1:
                        print(date, priceQ, priceM, stkQ, stkM, cash, priceQ*stkQ + priceM*stkM + cash)

                bal = priceQ*stkQ + priceM*stkM + cash

                if bal > taMax:
                    taMax = bal

                if bal > balMax:
                    balMax = bal
                    tMax = t
                    arMax = a

        print('taMax', taMax, 't', t, 'a', a)

        dfT = pd.DataFrame({'t':t, 'a':a, 'bal':taMax}, index=[0])
        dfO = pd.concat([dfO,dfT], ignore_index=True, axis=0)

print('balMax', balMax, 'tMax', tMax, 'arMax', arMax)

dfO.to_csv('5jlRbl.csv', index=True)
