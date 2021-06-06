#!/bin/sh
python drop_db.py
python create_db.py
python populate_stocks.py
python populate_prices.py
#python populate_earnings.py # TODO