import ccxt
import time
import datetime as dt
from time import sleep
from datetime import timedelta
from notification import notificator
from exchange import exchange, api_requests_frequency
from market_data import check_coin_price
from config import get_config
from balance import fetch_balance

show_error = "YES"

exchange = exchange()
api_requests_frequency = api_requests_frequency()

use_limit_orders = get_config()["use_limit_orders"]
exchange_fee = float(get_config()["exchange_fee"])

use_bnb_for_fee = get_config()["use_bnb_for_fee"]

coin_2 = get_config()["coin_2"].upper()
start_balance = fetch_balance(coin_2)

cancel_order_by_time = get_config()["cancel_order_by_time"]
time_to_cancel_order_by_inactivity_minutes = int(
    get_config()["time_to_cancel_order_by_inactivity_minutes"]
)


total_profit_for_this_session = 0.0
balance_on_session_start = start_balance

number_failed_connect_to_billing_server = 0


def calculate_amount_to_by(coin_pair, stake_per_trade, coin_2, current_price):

    global number_failed_connect_to_billing_server

    try:
        current_balance_coin_2 = fetch_balance(coin_2)
        if use_limit_orders == "YES":
            coin_price = current_price
        else:
            coin_price = check_coin_price(coin_pair)

        if current_balance_coin_2 < stake_per_trade:
            amount = current_balance_coin_2 / coin_price
        else:
            amount = stake_per_trade / coin_price

        amount_str = str(amount)
        dot_pos = amount_str.find(".")
        amount = float(amount_str[: dot_pos + 8])
        return amount

    except ccxt.NetworkError as e:
        if show_error == "YES":
            notificator(str(e))
    except ccxt.ExchangeError as e:
        if show_error == "YES":
            notificator(str(e))
    except Exception as e:
        if show_error == "YES":
            notificator(str(e))


def calculate_amount_to_sell(buy_order, coin):

    buy_size = float(buy_order["filled"])

    if use_bnb_for_fee == "YES" and buy_size <= fetch_balance(coin):
        to_sell = buy_size

    else:
        buy_size_with_fee = buy_size - ((buy_size / 100) * exchange_fee)
        to_sell = buy_size_with_fee

    to_sell_str = str(to_sell)
    dot_pos = to_sell_str.find(".")
    to_sell = float(to_sell_str[: dot_pos + 8])
    return to_sell


def calculate_profit(coin_2):
    global start_balance
    global total_profit_for_this_session

    now_balance_coin_2 = fetch_balance(coin_2)

    profit = now_balance_coin_2 - start_balance

    total_profit_for_this_session = total_profit_for_this_session + profit

    # percents
    prof_in_percents = (profit * 100) / start_balance
    tot_prof_in_percents = (
        total_profit_for_this_session * 100
    ) / balance_on_session_start

    start_balance = now_balance_coin_2

    return profit, total_profit_for_this_session, prof_in_percents, tot_prof_in_percents


def make_order(coin_pair, type_ord, side, amount, price):
    try:
        symbol = coin_pair
        type_o = type_ord  # "market" or "limit"
        side = side  # "buy" or "sell"
        amount = amount
        price = price
        params = {}
        order = (symbol, type, side, amount, price, params)
        order = exchange.create_order(symbol, type_o, side, amount, price, params)
        return order

    except ccxt.NetworkError as e:
        if show_error == "YES":
            notificator(str(e))
    except ccxt.ExchangeError as e:
        if show_error == "YES":
            notificator(str(e))
    except Exception as e:
        if show_error == "YES":
            notificator(str(e))


def fetch_filled_price_by_id(order_id, coin_pair):
    try:
        if exchange.has["fetchOrder"]:
            filled_order_price_dict = exchange.fetchOrder(
                id=order_id, symbol=coin_pair, params={}
            )
            return filled_order_price_dict["price"]

    except ccxt.NetworkError as e:
        if show_error == "YES":
            notificator(str(e))
    except ccxt.ExchangeError as e:
        if show_error == "YES":
            notificator(str(e))
    except Exception as e:
        if show_error == "YES":
            notificator(str(e))


def fetch_order_cost_by_id(order_id, coin_pair):
    try:
        if exchange.has["fetchOrder"]:
            filled_order_cost_dict = exchange.fetchOrder(
                id=order_id, symbol=coin_pair, params={}
            )
            return filled_order_cost_dict["cost"]

    except ccxt.NetworkError as e:
        if show_error == "YES":
            notificator(str(e))
    except ccxt.ExchangeError as e:
        if show_error == "YES":
            notificator(str(e))
    except Exception as e:
        if show_error == "YES":
            notificator(str(e))


def check_order_status_by_id(order_id, coin_pair):
    try:
        while True:

            if exchange.has["fetchOrder"]:
                filled_order_status_dict = exchange.fetchOrder(
                    id=order_id, symbol=coin_pair, params={}
                )
                if filled_order_status_dict["status"] == "open":
                    if cancel_order_by_time == "YES":
                        cancel_limit_order_by_inactivity(order_id, coin_pair)
                        time.sleep(api_requests_frequency)
                        continue
                    else:
                        time.sleep(api_requests_frequency)
                        continue

                if filled_order_status_dict["status"] == "canceled":
                    return "canceled"
                    break

                if filled_order_status_dict["status"] == "closed":
                    return "closed"
                    break

    except ccxt.NetworkError as e:
        if show_error == "YES":
            notificator(str(e))
    except ccxt.ExchangeError as e:
        if show_error == "YES":
            notificator(str(e))
    except Exception as e:
        if show_error == "YES":
            notificator(str(e))


def fetch_full_closed_order_by_id(order_id, coin_pair):
    try:
        if exchange.has["fetchOrder"]:
            full_closed_order_cost_dict = exchange.fetchOrder(
                id=order_id, symbol=coin_pair, params={}
            )
            return full_closed_order_cost_dict

    except ccxt.NetworkError as e:
        if show_error == "YES":
            notificator(str(e))
    except ccxt.ExchangeError as e:
        if show_error == "YES":
            notificator(str(e))
    except Exception as e:
        if show_error == "YES":
            notificator(str(e))


def fetch_filled_order_amount_by_id(order_id, coin_pair):
    try:
        if exchange.has["fetchOrder"]:
            filled_order_cost_dict = exchange.fetchOrder(
                id=order_id, symbol=coin_pair, params={}
            )
            return filled_order_cost_dict["filled"]

    except ccxt.NetworkError as e:
        if show_error == "YES":
            notificator(str(e))
    except ccxt.ExchangeError as e:
        if show_error == "YES":
            notificator(str(e))
    except Exception as e:
        if show_error == "YES":
            notificator(str(e))


def check_order_date_time_by_id(order_id, coin_pair):
    try:
        if exchange.has["fetchOrder"]:
            order_datetime_dict = exchange.fetchOrder(
                id=order_id, symbol=coin_pair, params={}
            )
            order_datetime = order_datetime_dict["datetime"]
            order_datetime = order_datetime.replace("T", " ")
            order_datetime = order_datetime.replace("Z", "")
            return order_datetime

    except ccxt.NetworkError as e:
        if show_error == "YES":
            notificator(str(e))
    except ccxt.ExchangeError as e:
        if show_error == "YES":
            notificator(str(e))
    except Exception as e:
        if show_error == "YES":
            notificator(str(e))


def cancel_limit_order_by_inactivity(order_id, coin_pair):

    # here using datetime.utcnow() insted datetime.now()
    # because binance has UTC time, and gives orders time in UTC

    params = {}

    try:
        order_datetime = check_order_date_time_by_id(order_id, coin_pair)
        tm_inact = time_to_cancel_order_by_inactivity_minutes

        order_date = dt.datetime.fromisoformat(order_datetime) + timedelta(
            minutes=tm_inact
        )

        if order_date < dt.datetime.utcnow():
            exchange.cancel_order(order_id, coin_pair, params)

    except ccxt.NetworkError as e:
        notificator(str(e))
    except ccxt.ExchangeError as e:
        notificator(str(e))
    except Exception as e:
        notificator(str(e))
