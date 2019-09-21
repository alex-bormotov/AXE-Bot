import ccxt
from exchange import exchange
from notification import notificator

show_error = "YES"

exchange = exchange()


def fetch_ticker(coin_pair):
    try:
        response = exchange.fetch_ticker(coin_pair)["symbol"]
        notificator(response)
        return response

    except ccxt.NetworkError as e:
        if show_error == "YES":
            notificator(str(e))
    except ccxt.ExchangeError as e:
        if show_error == "YES":
            notificator(str(e))
    except Exception as e:
        if show_error == "YES":
            notificator(str(e))
