import sqlite3, config
import alpaca_trade_api as tradeapi
import tulipy
import numpy
from datetime import date
import pandas as pd

print('Start populating prices')
connection = sqlite3.connect('app.db')

connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    SELECT id, symbol, name FROM stock
""")

rows = cursor.fetchall()

current_date = date.today().isoformat() # TODO - CHANGE DATE ON WEEKDAYS, no data so it can't fetch the latest date
symbols = []
stock_dict = {}
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

chunk_size = 200
for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i:i+chunk_size]
    barsets = api.get_barset(symbol_chunk, 'day', 200)

    for symbol in barsets:
        #print(f"processing symbol {symbol}")
        recent_closes = [bar.c for bar in barsets[symbol]]
        for bar in barsets[symbol]:
            stock_id = stock_dict[symbol]
            if len(recent_closes) >= 50 and current_date == bar.t.date().isoformat():
                # triple ma
                sma_4 = tulipy.sma(numpy.array(recent_closes), period=4)[-1]
                sma_9 = tulipy.sma(numpy.array(recent_closes), period=9)[-1]
                sma_18 = tulipy.sma(numpy.array(recent_closes), period=18)[-1]
                rsi_14 = tulipy.rsi(numpy.array(recent_closes), period=14)[-1]
                # double ma
                if len(recent_closes) >= 200:
                    sma_21 = tulipy.sma(numpy.array(recent_closes), period=21)[-1]
                    sma_50 = tulipy.sma(numpy.array(recent_closes), period=50)[-1]
                    sma_200 = tulipy.sma(numpy.array(recent_closes), period=200)[-1]
            else:
                sma_4, sma_9, sma_18, sma_21, sma_50, sma_200, rsi_14 = None, None, None, None, None, None, None
            cursor.execute("""
                INSERT INTO stock_price (stock_id, date, open, high, low, close, volume, sma_4, sma_9, sma_18, sma_21, sma_50, sma_200, rsi_14)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v, sma_4, sma_9, sma_18, sma_21, sma_50, sma_200, rsi_14))
print('Done populating prices')
connection.commit()