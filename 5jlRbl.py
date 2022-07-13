"""
Ticker: TQQQ, TMF
Threshold: 1 to 10 percent
AmountRate: 10 ~ 90 percent
=> Price: Open
FeeRate: 0.07 percent
=> Rebalance at Threshold!
"""

import pandas as pd

file = open('transactionLog.txt', 'w')  # opening a file

dfQ = pd.read_csv("tqqq_5min.csv")
dfM = pd.read_csv("tmf_5min.csv")

threshold= [(1/1000) * x for x in range(150,351)]
amountRate = [(1/100) * x for x in range(100,101)]
feeRate = 0.0007

capital = 10000
balMax = 0
balCurr = 0
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
#            for p in ['Open']:
            for p in ['Open', 'Close']:
                srQ = dfQ.iloc[i]
                priceQ = srQ[p]
                date = srQ[0]
                srM = dfM.iloc[i]
                priceM = srM[p]

                gap = priceQ/tPriceQ - priceM/tPriceM

#                if len(threshold)==1 and len(amountRate)==1:
#                    print(gap)

                if gap > t:
                    amountQ = int(stkQ * a)
                    stkQ -= amountQ
                    cash += (priceQ * amountQ) * (1 - feeRate)
                    amountM = int(cash / (1 + feeRate) / priceM)
                    stkM += amountM
                    cash -= (priceM * amountM) * (1 + feeRate)

                    tPriceQ = priceQ
                    tPriceM = priceM

                    if len(threshold)==1 and len(amountRate)==1:
                        L = str(date) + str("%6.2f"%(priceQ)) + str("%6.2f"%(priceM)) + str("%7d"%(stkQ)) + str("%7d"%(stkM)) + str("%6.2f"%(cash)) + str("%8d"%(priceQ*stkQ + priceM*stkM + cash)) + "\n"
                        file.write(L)

                if gap < -t:
                    amountM = int(stkM * a)
                    stkM -= amountM
                    cash += (priceM * amountM) * (1 - feeRate)
                    amountQ = int(cash / (1 + feeRate) / priceQ)
                    stkQ += amountQ
                    cash -= (priceQ * amountQ) * (1 + feeRate)

                    tPriceQ = priceQ
                    tPriceM = priceM

                    if len(threshold)==1 and len(amountRate)==1:
                        L = str(date) + str("%6.2f"%(priceQ)) + str("%6.2f"%(priceM)) + str("%7d"%(stkQ)) + str("%7d"%(stkM)) + str("%6.2f"%(cash)) + str("%8d"%(priceQ*stkQ + priceM*stkM + cash)) + "\n"
                        file.write(L)

                bal = priceQ*stkQ + priceM*stkM + cash

                if taMax < bal:
                    taMax = bal

                if balMax < bal:
                    balMax = bal
                    tMax = t
                    arMax = a

        print('taMax', "%8d"%(taMax), 'bal', "%8d"%(bal), 't', "%5.3f"%(t), 'a', "%4.2f"%(a))

        if len(threshold)==1 and len(amountRate)==1:
            L = 'taMax' + str("%8d"%(taMax)) + ' bal' + str("%8d"%(bal)) + ' t' + str("%5.3f"%(t)) + ' a' + str("%4.2f"%(a)) + "\n"
            file.write(L)

        dfT = pd.DataFrame({'t':"%5.3f"%(t), 'a':"%4.2f"%(a), 'taMax':"%8d"%(taMax), 'bal':"%8d"%(bal)}, index=[0])
        dfO = pd.concat([dfO,dfT], ignore_index=True, axis=0)

        if balCurr < bal:
            balCurr = bal
            tCurr = t
            aCurr =a

if len(threshold)!=1 or len(amountRate)!=1:
    print('balCurr', "%8d"%(balCurr), 'tCurr', "%5.3f"%(tCurr), 'aCurr', "%4.2f"%(aCurr))
    print('balMax', "%8d"%(balMax), 'tMax', "%5.3f"%(tMax), 'arMax', "%4.2f"%(arMax))
    dfO.to_csv('5jlRbl.csv', index=False)

if len(threshold)==1 and len(amountRate)==1:
    file.close()
