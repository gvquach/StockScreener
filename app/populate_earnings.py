import sqlite3, config
import datetime
from datetime import date
from yahoo_earnings_calendar import YahooEarningsCalendar
from pandas.tseries.offsets import BDay

print('Start populating earnings')

days_out = 30

connection = sqlite3.connect('app.db')

connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    select max(date) from stock_price
""")

current_date = cursor.fetchone()['max(date)']

cursor.execute("""
    SELECT id, symbol, name FROM stock
""")


rows = cursor.fetchall()

dt_current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
dt_future_date = dt_current_date + BDay(days_out)

yec = YahooEarningsCalendar()
interval_data = yec.earnings_between(dt_current_date, dt_future_date)
print('Stored populating earnings')
symbols = []
stock_dict = {}
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']

for stock in interval_data:
    if stock['ticker'] in stock_dict:
        symbol = stock['ticker']
        #print(f"processing symbol {symbol}")
        pulled_date = stock['startdatetime']
        formatted_date = datetime.datetime.strptime(pulled_date,"%Y-%m-%dT%H:%M:%S.%fZ")
        cursor.execute("""
            UPDATE stock
            SET earnings_date = ?
            WHERE id = ?
        """,(formatted_date.date(), stock_dict[symbol]))

print('Done populating earnings')
connection.commit()