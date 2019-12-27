import time
import json
import requests
import pandas as pd
import datetime as dt
from time import sleep
from notification import notificator
from requests.adapters import HTTPAdapter
from exchange import api_requests_frequency

show_error = "YES"
api_requests_frequency = api_requests_frequency()


# GET PRICE FROM CRYPTOWAT.CH:
def check_coin_price(coin_pair_for_get_bars):
    def get_price():
        # https://developer.cryptowat.ch/reference/rest-api-getting-started
        root_url = "https://api.cryptowat.ch/markets/binance/"
        url = root_url + coin_pair_for_get_bars.lower() + "/price"
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        req_session = requests.Session()
        req_session.headers.update({"User-Agent": user_agent})
        req_session.mount(url, HTTPAdapter(max_retries=3))

        try:
            while True:
                req = req_session.get(url, headers={"User-Agent": user_agent})
                if req.ok:
                    if 'price' in req_session.get(url, headers={"User-Agent": user_agent}).text:
                        price = json.loads(req.text)["result"]["price"]
                        if type(price) is int or type(price) is float:
                            return float(price)
                            break
                        else:
                            time.sleep(api_requests_frequency)
                            continue
                    else:
                        time.sleep(api_requests_frequency)
                        continue
                else:
                    time.sleep(api_requests_frequency)
                    continue
        except Exception:
            pass

    while True:
        price = get_price()
        if price is not None:
            return(price)
            break
        else:
            continue


# GET DATA FROM CRYPTOWAT.CH:
def get_bars(symbol, interval):
    # https://developer.cryptowat.ch/reference/rest-api-getting-started
    if interval == "1m":
        periods_seconds = 60
    if interval == "5m":
        periods_seconds = 300
    if interval == "15m":
        periods_seconds = 900
    if interval == "30m":
        periods_seconds = 1800
    if interval == "1h":
        periods_seconds = 3600
    if interval == "4h":
        periods_seconds = 14400
    if interval == "1d":
        periods_seconds = 86400

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    url = f'https://api.cryptowat.ch/markets/binance/{symbol.lower()}/ohlc?periods={periods_seconds}'
    req_session = requests.Session()
    req_session.headers.update({"User-Agent": user_agent})
    req_session.mount(url, HTTPAdapter(max_retries=3))

    try:
        req = req_session.get(url, headers={"User-Agent": user_agent})

        if req.ok:
            df = pd.DataFrame(json.loads(req.text)["result"][str(periods_seconds)])
            df.columns = [
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "qav",
            ]
            df.index = [dt.datetime.fromtimestamp(x) for x in df.open_time]
            df.open = df.open.astype(float)
            df.close = df.close.astype(float)

            return df

    except Exception as e:
        if show_error == "YES":
            notificator(str(e) + ' from get_bars' + ' df ' + str(df))


# GET PRICE FROM BINANCE (CCXT):
# from exchange import exchange
# exchange = exchange()

# def check_coin_price(coin_pair):
#     try:
#         return exchange.fetch_ticker(coin_pair)["last"]
#
#     except Exception as e:
#         if show_error == "YES":
#             notificator(f'coin_pair must be like ETH/USDT (for CCXT), received {coin_pair}')
#             notificator(
#                 str(e) + " this shit happened in market_data.py (check_coin_price)"
#             )

# GET PRICE FROM BINANCE (requests):
# def check_coin_price(coin_pair_for_get_bars):
#     root_url = "https://api.binance.com/api/v3/ticker/24hr?symbol="
#     url = root_url + coin_pair_for_get_bars
#     user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
#
#     req_session = requests.Session()
#     req_session.headers.update({"User-Agent": user_agent})
#     req_session.mount(url, HTTPAdapter(max_retries=3))
#
#     try:
#         req = req_session.get(url, headers={"User-Agent": user_agent})
#         price = json.loads(req.text)["lastPrice"]
#         return price
#
#     except Exception as e:
#         if show_error == "YES":
#             notificator(f'coin_pair must be like ETHUSDT, received {coin_pair_for_get_bars}')
#             notificator(
#                 str(e) + " this shit happened in market_data.py (check_coin_price)"
#             )


# GET DATA FROM BINANCE:
# def get_bars(symbol, interval):
#     root_url = "https://api.binance.com/api/v1/klines"
#     user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
#     url = root_url + "?symbol=" + symbol + "&interval=" + interval
#
#     req_session = requests.Session()
#     req_session.headers.update({"User-Agent": user_agent})
#     req_session.mount(url, HTTPAdapter(max_retries=3))
#
#     try:
#         req = req_session.get(url, headers={"User-Agent": user_agent})
#
#         if req.ok:
#             df = pd.DataFrame(json.loads(req.text))
#             df.columns = [
#                 "open_time",
#                 "open",
#                 "high",
#                 "low",
#                 "close",
#                 "volume",
#                 "close_time",
#                 "qav",
#                 "num_trades",
#                 "taker_base_vol",
#                 "taker_quote_vol",
#                 "ignore",
#             ]
#             df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.close_time]
#             df.open = df.open.astype(float)
#             df.close = df.close.astype(float)
#
#             return df
#
#     except Exception as e:
#         if show_error == "YES":
#             notificator(str(e))
