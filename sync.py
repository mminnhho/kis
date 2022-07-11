import pandas as pd


def sync(tickerA, tickerB):

    print('syncing...')

    dfA = pd.read_csv(tickerA + '.csv')
    dfB = pd.read_csv(tickerB + '.csv')
    dfO = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

    beginPointer = 0

    for i in range(0, len(dfA)):
        srA = dfA.iloc[i]

        for j in range(beginPointer, len(dfB)):
            srB = dfB.iloc[j]

            if srA[0] == srB[0]:
                dfT = pd.DataFrame({'Date':[srA[0]], 'Open':[srA[1]], 'High':[srA[2]], 'Low':[srA[3]], 'Close':[srA[4]], 'Adj Close':[srA[5]], 'Volume':[srA[6]]})
                dfO = pd.concat([dfO,dfT], ignore_index=True, axis=0)
                beginPointer = j + 1

#            elif srA[0] < srB[0]:
            elif srA[0] != srB[0]:
                break

    dfO.to_csv(tickerA + '.csv', index=False)


def main(tickerA, tickerB):
    sync(tickerA, tickerB)
    sync(tickerB, tickerA)


tickerA = 'tqqq_10min'
tickerB = 'tmf_10min'

main(tickerA, tickerB)
