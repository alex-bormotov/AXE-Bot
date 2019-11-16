import ccxt
import time
import json
import requests
import pandas as pd
import datetime as dt
from datetime import timedelta
from exchange import exchange
from notification import notificator
from requests.adapters import HTTPAdapter

show_error = "YES"

exchange = exchange()


def check_coin_price(coin_pair):
    try:
        last_price = exchange.fetch_ticker(coin_pair)["last"]
        return last_price

    except ccxt.NetworkError as e:
        if show_error == "YES":
            notificator(str(e))
    except ccxt.ExchangeError as e:
        if show_error == "YES":
            notificator(str(e))
    except Exception as e:
        if show_error == "YES":
            notificator(str(e))


def get_bars(symbol, interval):
    req_session = requests.Session()
    root_url = "https://api.binance.com/api/v1/klines"

    try:
        url = root_url + "?symbol=" + symbol + "&interval=" + interval
        headers = requests.utils.default_headers()
        headers[
            "User-Agent"
        ] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"

        while True:
            req_session.mount(url, HTTPAdapter(max_retries=19))
            request = req_session.get(url, headers=headers)

            if request.ok and request.text != None:
                df = pd.DataFrame(json.loads(request.text))
                df.columns = [
                    "open_time",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "close_time",
                    "qav",
                    "num_trades",
                    "taker_base_vol",
                    "taker_quote_vol",
                    "ignore",
                ]
                df.index = [
                    dt.datetime.fromtimestamp(x / 1000.0) for x in df.close_time
                ]
                df.open = df.open.astype(float)
                df.close = df.close.astype(float)
                return df
                break
            else:
                time.sleep(5)
                continue

    except Exception as e:
        if show_error == "YES":
            notificator(str(e))
