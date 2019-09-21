import ccxt
import time
import json
import requests
import pandas as pd
import datetime as dt
from datetime import timedelta
from exchange import exchange
from notification import notificator

show_error = "YES"

exchange = exchange()

df_load_already = False
df_global = None
df_datetime = dt.datetime.utcnow()


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

    global df_load_already
    global df_global
    global df_datetime

    if df_datetime + timedelta(seconds=20) < dt.datetime.utcnow():
        df_load_already = False
        df_datetime = dt.datetime.utcnow()

    if df_load_already == False:

        try:
            headers = requests.utils.default_headers()
            headers[
                "User-Agent"
            ] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
            root_url = "https://api.binance.com/api/v1/klines"
            url = root_url + "?symbol=" + symbol + "&interval=" + interval
            while True:
                try:
                    data = json.loads(requests.get(url, headers=headers).text)
                    break
                except requests.exceptions.RequestException:
                    continue

            df = pd.DataFrame(data)
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
            df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.close_time]
            df.open = df.open.astype(float)
            df.close = df.close.astype(float)

            df_load_already = True
            df_global = df
            return df_global

        except requests.exceptions.RequestException as e:
            if show_error == "YES":
                notificator(str(e))
        except ccxt.NetworkError as e:
            if show_error == "YES":
                notificator(str(e))
        except ccxt.ExchangeError as e:
            if show_error == "YES":
                notificator(str(e))
        except Exception as e:
            if show_error == "YES":
                notificator(str(e))

    else:
        return df_global
