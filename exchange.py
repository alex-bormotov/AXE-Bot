import ccxt
from config import get_config

show_error = "YES"


def exchange():
    try:
        key = get_config()["key"]
        secret = get_config()["secret"]
        exchange = ccxt.binance(
            {"apiKey": key, "secret": secret, "enableRateLimit": True}
        )
        return exchange

    except ccxt.NetworkError as e:
        if show_error == "YES":
            notificator(str(e))
    except ccxt.ExchangeError as e:
        if show_error == "YES":
            notificator(str(e))
    except Exception as e:
        if show_error == "YES":
            notificator(str(e))


def api_requests_frequency():
    api_requests_frequency = 0.5  # sec
    return api_requests_frequency
