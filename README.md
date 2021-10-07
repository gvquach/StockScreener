# NOTE: This repo has been depreprecated, Alpaca API has been updated to work differently.
# StockScreener

A full-stack web application that uses technical analysis and more to screen stocks for a nice view on a table.

## Features

Creates a SQLite database and populates the database with stock data. Now you can apply SQL queries and indicators to close in on data that satisfy your stock buy/sell requirements. Now you have tickers that you can use your brain along with many filters to choose what stocks to buy!

# Files

## Templates
| File                             |Description                                                                                                            |
| -------------------------------- |---------------------------------------------------------------------------------------------------------------------- |
| index.html                       |Table UI                                                                                                               |
| layout.html                      |UI container + Navbar, the theme UI                                                                                    |
| stock_detail.html                |Stock detail UI + TradingView chart widget                                                                             |
## .py files
| File                             |Description                                                                                                            |
| -------------------------------- |---------------------------------------------------------------------------------------------------------------------- |
| config.py                        |API keys                                                                                                               |
| create_db.py                     |Create the database                                                                                                    |
| drop_db.py                       |Drop the database                                                                                                      |
| main.py                          |Main file that serves the templates and responses                                                                      |
| populate_earnings.py             |Populate the earnings date in the stock table                                                                          |
| populate_prices.py               |Populate everything in the stock_price table                                                                           |
| populate_stocks.py               |Populate the stock/ticker in the stock table                                                                           |
## Shell scripts
| File                             |Description                                                                                                            |
| -------------------------------- |---------------------------------------------------------------------------------------------------------------------- |
| docker-rebuild.sh                |Reboots the docker image and container                                                                                 |
| init_data.sh                     |Runs all the necessary python scripts to restart our database                                                          |

## Configuration 

### Uvicorn

Run the 1st command in the root directory, 2nd command in the directory that contains main.py:    
```
$ pip3 install -r requirements.txt
$ uvicorn main:app --reload  
http://127.0.0.1:8000/
```

### Docker

Run the following command in the root directory:    
```
$ ./docker-rebuild.sh  
http://127.0.0.1/
```

### Digital Ocean App Platform

Push changes to the master branch  
Then inside the Digital Ocean console run:    
```
$ chmod +x init_data.sh
$ ./init_data.sh  
https://stock-app-zkqzz.ondigitalocean.app/
```

## Built With

* Python
* Jinja2
* FastAPI
* Docker
* SQLite
* Semantic UI
* Bash
* HTML
* Digital Ocean App Platform

