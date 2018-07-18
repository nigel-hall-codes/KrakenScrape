import krakenex
import pandas as pd
import sqlite3
import models



kraken = krakenex.API()
#
#
# response = kraken.query_public('Depth', {'pair': 'ETHXBT', 'count': '100'})
# print(response)


def depth(pairs):
    df = pd.DataFrame(columns=["price", "volume", "timestamp", "type", "pair"])
    for pair in pairs:
        response = kraken.query_public("Depth", {"pair": pair})['result']
        cdf = response[list(response.keys())[0]]
        asks = cdf['asks']
        bids = cdf['bids']
        bids = pd.DataFrame(bids, columns=["price", "volume", "timestamp"])
        bids['type'] = "bid"
        asks = pd.DataFrame(asks, columns=["price", "volume", "timestamp"])
        asks['type'] = "ask"
        cdf = pd.concat([bids, asks])
        cdf['pair'] = pair
        df = pd.concat([df, cdf])


    return df



def download_depth_chart(pairs):
    conn = sqlite3.connect('crypto.db')
    df = depth(pairs)
    df.to_sql('orderbook', con=conn, if_exists='append')
    print("sraped")



def ticker(pairs):
    master_df = pd.DataFrame()
    for pair in pairs:
        finalDict = {}
        response = kraken.query_public("Ticker", {"pair": pair})['result']
        cDict = response[list(response.keys())[0]]
        print(cDict)
        finalDict['pair'] = pair
        finalDict['volume_weighted_avg_price_today'] = cDict['p'][0]
        finalDict["volume_weighted_avg_price_last24"] = cDict['p'][1]
        finalDict["volume_today"] = cDict['v'][0]
        finalDict["volume_last24"] = cDict['v'][1]
        finalDict["ask_price"] = cDict['a'][0]
        finalDict["ask_whole_lot_volume"] = cDict['a'][1]
        finalDict["bid_price"] = cDict['b'][0]
        finalDict["bid_lot_volume"] = cDict['b'][1]
        finalDict["todays_opening_price"] = cDict['o']
        finalDict["high_today"] = cDict['h'][0]
        finalDict["high_last24 "] = cDict['h'][1]
        finalDict["low_today"] = cDict['l'][0]
        finalDict["low_last24"] = cDict['l'][1]
        finalDict["number_of_trades_today"] = cDict['t'][0]
        finalDict["number_of_trades_last24"] = cDict['t'][1]
        for key in finalDict:
            finalDict[key] = [finalDict[key]]
        df = pd.DataFrame(finalDict)
        master_df = pd.concat([master_df, df])
    master_df = master_df.set_index("pair")



    return master_df


# download_depth_chart(["ETHUSD"])

# print(depth(['ETHUSD']))



