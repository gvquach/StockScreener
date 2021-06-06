import sqlite3, config
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse
from datetime import date
import datetime
from pandas.tseries.offsets import BDay

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    stock_filter = request.query_params.get('filter', False)

    connection = sqlite3.connect('app.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""
        select max(date) from stock_price
    """)

    current_date = cursor.fetchone()['max(date)']
    dt_current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
    dt_future_date = dt_current_date + BDay(30)
    future_date = dt_future_date.date()
    current_date = dt_current_date.date()

    if stock_filter == 'Indicator_Combo':
        cursor.execute("""
            select symbol, name, stock_id, date, stock.id
            from stock_price join stock on stock.id = stock_price.stock_id
            where close > sma_21
            AND rsi_14 BETWEEN 50 AND 55
            AND date = (select max(date) from stock_price)
            order by symbol
        """)
    elif stock_filter == 'TMA_Bullish':
        cursor.execute("""
            select symbol, name, stock_id, date, stock.id
            from stock_price join stock on stock.id = stock_price.stock_id
            where close > sma_21
            AND date = (select max(date) from stock_price)
            order by symbol
        """)
    elif stock_filter == 'DMA_Bullish':
        cursor.execute("""
            select symbol, name, stock_id, date, stock.id
            from stock_price join stock on stock.id = stock_price.stock_id
            where sma_21 > sma_50
            OR sma_50 > sma_200
            AND date = (select max(date) from stock_price)
            order by symbol
        """)
    elif stock_filter == 'earnings_before_3w':
        cursor.execute("""
            select symbol, name, stock_id, earnings_date, stock.id
            from stock_price join stock on stock.id = stock_price.stock_id
            where earnings_date BETWEEN ? AND ?
            AND date = (select max(date) from stock_price)
            order by earnings_date
        """,(current_date, future_date,))
    elif stock_filter == 'all_stocks':
        cursor.execute("""
            select symbol, name, stock_id, earnings_date, stock.id
            from stock_price join stock on stock.id = stock_price.stock_id
            AND date = (select max(date) from stock_price)
            order by symbol
        """)
    rows = cursor.fetchall()

    cursor.execute("""
        select symbol,
        sma_4, 
        sma_9, 
        sma_18, 
        sma_21, 
        sma_50, 
        sma_200,
        rsi_14, 
        close,
        earnings_date
        from stock join stock_price on stock_price.stock_id = stock.id
        where date = (select max(date) from stock_price)
    """)

    indicator_rows = cursor.fetchall()
    indicator_values = {}

    for row in indicator_rows:
        indicator_values[row['symbol']] = row

    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows, "indicator_values": indicator_values , "date": current_date})

@app.get("/stock/{symbol}")
def stock_detail(request: Request, symbol):
    connection = sqlite3.connect('app.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, symbol, name FROM stock WHERE symbol = ?
    """, (symbol,))

    row = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM stock_price WHERE stock_id = ? ORDER BY date DESC
    """, (row['id'],))

    prices = cursor.fetchall()
    return templates.TemplateResponse("stock_detail.html", {"request": request, "stock": row, "bars": prices})

@app.get('/app.db')
def download_db():
    return FileResponse('app.db')