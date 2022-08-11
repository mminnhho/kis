import pandas as pd
import random

def sellBuy(v0, v1, v2, v3, v4, v5, v6):
    if not (v4==0 and v5!=0):
        v6 += (v0*v4) * (1-feeRate)
        v4 = 0
        v5 = int(v6/(1+feeRate) / v1)
        v6 -= (v1*v5) * (1+feeRate)
    v2 = v0
    v3 = v1
    return v0, v1, v2, v3, v4, v5, v6

def logging(dateBegin, dateEnd, tMaxT, yMaxT, tMaxDT, yMaxDt, dfO):
    dfT = pd.DataFrame({'begin':dateBegin, 'end':dateEnd, \
                        'tMaxT':"%5.3f"%(tMaxT), 'yMaxT':"%7.2f"%(yMaxT), \
                        'tMaxDT':"%5.3f"%(tMaxDT), 'yMaxDT':"%7.2f"%(yMaxDT)}, index=[0])
    dfO = pd.concat([dfO,dfT], ignore_index=True, axis=0)
    print(dateBegin, dateEnd, 'tMaxT', "%5.3f"%(tMaxT), 'yMaxT', "%7.2f"%(yMaxT), \
                              'tMaxDT', "%5.3f"%(tMaxDT), 'yMaxDT', "%7.2f"%(yMaxDT))
    return dfO

def loggingTransaction(date, gap, priceA, priceB, stkA, stkB, cash):
    if (len(dateB)==1) and (len(threshold)==1):
#    if True:
        L = date + str("%6.1f"%(gap*100)) + "%" + \
                   str("%6.2f"%(priceA)) + str("%6.2f"%(priceB)) + \
                   str("%7d"%(stkA)) + str("%7d"%(stkB)) + \
                   str("%9.2f"%(cash)) + str("%8d"%(priceA*stkA + priceB*stkB + cash)) + "\n"
        file.write(L)

dfA = pd.read_csv("tqqq.csv")
dfB = pd.read_csv("tmf.csv")
threshold = [(1/1000) * r for r in range(10,501,10)]
dateB = [*range(0,1)]  # begining date
feeRate = 0.0007
capital = 10000
cashflow = 0
sumCashflow = 0
dfO = pd.DataFrame(columns = ['begin', 'end', 'tMaxT', 'yMaxT', 'tMaxDT', 'yMaxDT'])
file = open('28jul_transaction.txt', 'w')

for l in range(0,1):  # repeat times

    for i in dateB:  # begining date
        tMaxDT = 0
        balMaxDT = 0
        yMaxDT = 0

        for t in threshold:
            balMaxT = 0
            tMaxT = 0
            stkA, stkB = 0, 0
            cash = capital
            srA = dfA.iloc[i]
            tPriceA = srA[4]
            srB = dfB.iloc[i]
            tPriceB = srB[4]
            dateBegin = srA[0]
            prd = pd.Period(dateBegin, freq='S')
            previousMonth = prd.month

            for j in range(i+1,len(dfA)):
                srA = dfA.iloc[j]
                srB = dfB.iloc[j]
                date = srA[0]
                prd = pd.Period(date, freq='S')
                month = prd.month
                if month != previousMonth:
                    cash += cashflow
                    sumCashflow += cashflow
                    previousMonth = month
                if date > dateBegin:
                    dateEnd = date

                for p in ['Open', 'Close']:  # day chart
#                for p in ['Open']:  # 1h, 10min chart
                    priceA = srA[p]
                    priceB = srB[p]
                    gap = priceA/tPriceA - priceB/tPriceB
#                    tr = t - 0.0003 + random.random()*0.0006  # randomizing the threshold
                    tr = t
                    if gap > tr:
                        (priceA, priceB, tPriceA, tPriceB, stkA, stkB, cash) = \
                                sellBuy(priceA, priceB, tPriceA, tPriceB, stkA, stkB, cash)
                        loggingTransaction(date, gap, priceA, priceB, stkA, stkB, cash)

                    if gap < -tr:
                        (priceB, priceA, tPriceB, tPriceA, stkB, stkA, cash) = \
                                sellBuy(priceB, priceA, tPriceB, tPriceA, stkB, stkA, cash)
                        loggingTransaction(date, gap, priceA, priceB, stkA, stkB, cash)

                    bal = priceA*stkA + priceB*stkB + cash
                    if balMaxT < bal:
                        balMaxT = bal
                        yMaxT = balMaxT / (capital+sumCashflow)
                        tMaxT = t
                    if balMaxDT < balMaxT:
                        balMaxDT = balMaxT
                        yMaxDT = balMaxDT / (capital+sumCashflow)
                        tMaxDT = tMaxT

            dfO = logging(dateBegin, dateEnd, tMaxT, yMaxT, tMaxDT, yMaxDT, dfO)
            loggingTransaction(date, gap, priceA, priceB, stkA, stkB, cash)

        tMaxT, yMaxT = 0, 0
        dfO = logging(dateBegin, dateEnd, tMaxT, yMaxT, tMaxDT, yMaxDT, dfO)

dfO.to_csv('28jul_AoN_threshold.csv', index=False)

L = 'meanThreshold ' + "%5.1f"%(dfO['tMaxDT'].astype(float).mean()*100) + '%' + '\n'
file.write(L)
L = 'maxYield     ' + str("%7.2f"%(dfO['yMaxDT'].astype(float).max())) + '\n'
file.write(L)
L = 'minYield     ' + str("%7.2f"%(dfO['yMaxDT'].astype(float).min())) + '\n'
file.write(L)
L = 'medianYield  ' + str("%7.2f"%(dfO['yMaxDT'].astype(float).median())) + '\n'
file.write(L)
L = 'meanYield    ' + str("%7.2f"%(dfO['yMaxDT'].astype(float).mean())) + '\n'
file.write(L)
file.close()
