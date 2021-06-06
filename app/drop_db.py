import sqlite3
import config

connection = sqlite3.connect(config.DB_FILE)
    
cursor = connection.cursor()

cursor.execute("""
    DROP TABLE stock_price
""")

cursor.execute("""
    DROP TABLE stock
""")

print('Dropped table')
connection.commit()