import sqlite3, config
import alpaca_trade_api as tradeapi

print('Start populating stocks')

connection = sqlite3.connect('app.db')

connection.row_factory = sqlite3.Row

cursor = connection.cursor()

with open('../app/data/cboe_options.csv') as file:
    contents = file.read()


api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)
assets = api.list_assets()

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol in contents:
            #print(f"Added a new stock {asset.symbol}")
            cursor.execute("INSERT INTO stock (symbol, name, exchange) VALUES (?, ?, ?)", (asset.symbol, asset.name, asset.exchange))
    except Exception as e:
        print(asset.symbol)
        print(e)
print('Done populating stocks')
connection.commit()