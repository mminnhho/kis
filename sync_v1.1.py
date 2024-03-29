import pandas as pd

def sync(tickerA, tickerB):
    print('syncing...', tickerA, tickerB)
    dfA = pd.read_csv(tickerA + '.csv')
    dfB = pd.read_csv(tickerB + '.csv')
    dfO = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close'])
    beginPointer = 0
    for i in range(0, len(dfA)):
        srA = dfA.iloc[i]
        for j in range(beginPointer, len(dfB)):
            srB = dfB.iloc[j]
            if srA[0] == srB[0]:
                dfT = pd.DataFrame({'Date':[srA[0]], 'Open':[srA[1]], 'High':[srA[2]], \
                                    'Low':[srA[3]], 'Close':[srA[4]]})
                dfO = pd.concat([dfO,dfT], ignore_index=True, axis=0)
                beginPointer = j + 1
            if srA[0] < srB[0]:
                break
    dfO.to_csv(tickerA + '.csv', index=False)

list = ['TQQQ', 'SOXL', 'TMF', 'SQQQ']
for tickerA in list:
    for tickerB in list:
        if tickerA != tickerB:
            sync(tickerA, tickerB)
