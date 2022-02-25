from dis import Instruction
import ccxt
from connect import connect, connect_multi
import pandas as pd
from datetime import datetime
from psycopg2.extras import execute_values




##Preço atual dos ativos BTC, ETH, BNB, ADA e SOL

my_exchange = 'Binance' 
basebtc = 'BTC' 
quotebtc= 'USDT'
method_to_call = getattr(ccxt,my_exchange.lower()) 
exchange_obj = method_to_call() 
pair_price_data = exchange_obj.fetch_ticker(basebtc+'/'+quotebtc) 
closure_price_btc = pair_price_data['close']


#Inserir no banco
# insert_script = 'INSERT INTO ticker (base, quote, price) VALUES (%s, %s, %s)'
# insert_value = (basebtc, quotebtc, closure_price_btc)
# insertBTC = connect(insert_script, insert_value)



# Histórico de preços por intervalo de tempo

binance = ccxt.binance()

symbol = 'BTC/USDT'
ticker = '5m'
since = binance.parse8601('2022-02-19T21:00:00Z')
limit = 1000

binance.loadMarkets()
quotes = binance.fetch_ohlcv(symbol, ticker, since, limit)
 
def parserToDatetime(dataSet, dateTimeIndex):
    for element in dataSet:
        element[dateTimeIndex] = datetime.fromtimestamp(element[dateTimeIndex]/1000).strftime("%Y-%m-%d %H:%M:%S")
    return dataSet

def parserToFloat(dataSet, arrayFloatIndex):
    for element in dataSet:
        for index in arrayFloatIndex:
            element[index] = float(element[index])
    return dataSet

quotes = parserToDatetime(quotes, 0)
quotes = parserToFloat (quotes, [1,2,3,4,5])

connect_multi('INSERT INTO MULTI_TICKER(datetime, open, high, low, close, volume) VALUES ', quotes)


