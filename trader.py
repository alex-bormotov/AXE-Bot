import ccxt
import time
from time import sleep
from config import get_config
from notification import notificator
from exchange import exchange, api_requests_frequency
from orders import (
    calculate_amount_to_by,
    calculate_amount_to_sell,
    make_order,
    fetch_filled_price_by_id,
    calculate_profit,
    check_order_status_by_id,
    fetch_full_closed_order_by_id,
    fetch_filled_order_amount_by_id,
    check_order_date_time_by_id,
)
from dynamic_trail import dynamic_trail
from balance import check_balance_before_start, fetch_balance, get_stake_size
from error_handling import fetch_ticker
from db import save_result_to_sqlite, save_result_to_firebase
from market_data import check_coin_price
from indicators import get_indicators_signal, get_indicators_signal_sell
from human import number_for_human
from licence import show_bot_id

show_error = "YES"
debug = "NO"

api_requests_frequency = api_requests_frequency()
exchange = exchange()

save_to_sqlite = get_config()["save_to_sqlite"]
save_to_firebase = get_config()["save_to_firebase"]
start_sell_trail_on_sell_signal = get_config()["start_sell_trail_on_sell_signal"]
use_limit_orders = get_config()["use_limit_orders"]
use_all_balance = get_config()["use_all_balance"]
dynamic_trail_enable = get_config()["dynamic_trail_enable"]
start_buy_trail_on_buy_signal = get_config()["start_buy_trail_on_buy_signal"]
use_bnb_for_fee = get_config()["use_bnb_for_fee"]


def trail_buy(coin, coin_2, stake_per_trade):
    try:
        buy_trail_step = float(get_config()["buy_trail_step"])
        coin_pair = coin + "/" + coin_2
        coin_pair_for_get_bars = (
            coin + coin_2
        )  # another format(ETHBTC) then coin_pair(ETH/BTC) for ccxt
        notificator("Awaiting buy ...")
        start_price = check_coin_price(coin_pair_for_get_bars)
        time.sleep(1)
        current_price = check_coin_price(coin_pair_for_get_bars)
        current_change_percent = (
            (float(current_price) - start_price) / start_price
        ) * 100
        last_change_percent = current_change_percent

        while True:

            if last_change_percent + buy_trail_step >= current_change_percent:
                if last_change_percent > current_change_percent:
                    last_change_percent = current_change_percent

                current_price = check_coin_price(coin_pair_for_get_bars)
                current_change_percent = (
                    (float(current_price) - start_price) / start_price
                ) * 100

                if debug == "YES":
                    notificator(
                        "last_change_percent :\n"
                        + str(last_change_percent)[:9]
                        + "\n\n"
                        + "current_change_percent :\n"
                        + str(current_change_percent)[:9]
                        + "\n\n"
                        + "buy_trail_step :\n"
                        + str(buy_trail_step)
                    )

                time.sleep(api_requests_frequency)
                continue

            else:
                if use_limit_orders == "YES":

                    amount_to_buy = calculate_amount_to_by(
                        coin_pair, stake_per_trade, coin_2, current_price
                    )

                    buy_order_new = make_order(
                        coin_pair, "limit", "buy", amount_to_buy, current_price
                    )
                    buy_order_id = buy_order_new["id"]

                    if check_order_status_by_id(buy_order_id, coin_pair) == "canceled":
                        notificator("Buy order was canceled, restart ...")
                        start_again(coin_pair, coin, coin_2)
                        break

                    if check_order_status_by_id(buy_order_id, coin_pair) == "closed":
                        buy_order = fetch_full_closed_order_by_id(
                            buy_order_id, coin_pair
                        )
                        price_buy = fetch_filled_price_by_id(buy_order_id, coin_pair)
                        amount_filled = fetch_filled_order_amount_by_id(
                            buy_order_id, coin_pair
                        )
                        notificator(
                            "Buy (limit) "
                            + number_for_human(amount_filled)
                            + " "
                            + coin
                            + " at price "
                            + number_for_human(price_buy)
                            + " success"
                        )
                        if start_sell_trail_on_sell_signal == "YES":
                            notificator("Awaiting SELL signal ...")
                            if (
                                get_indicators_signal_sell(coin, coin_2, price_buy)[
                                    "signal"
                                ]
                                == "SELL"
                            ):
                                trail_sell(
                                    coin_pair,
                                    buy_order_id,
                                    price_buy,
                                    coin,
                                    coin_2,
                                    buy_order,
                                    stake_per_trade,
                                    coin_pair_for_get_bars,
                                )

                                break
                        trail_sell(
                            coin_pair,
                            buy_order_id,
                            price_buy,
                            coin,
                            coin_2,
                            buy_order,
                            stake_per_trade,
                            coin_pair_for_get_bars,
                        )

                        break
                else:
                    while True:
                        amount_to_buy = calculate_amount_to_by(
                            coin_pair, stake_per_trade, coin_2, current_price
                        )
                        buy_order = make_order(
                            coin_pair, "market", "buy", amount_to_buy, None
                        )
                        if buy_order is not None:
                            break
                        else:
                            continue

                    buy_order_id = buy_order["id"]
                    price_buy = fetch_filled_price_by_id(buy_order_id, coin_pair)
                    amount_filled = fetch_filled_order_amount_by_id(
                        buy_order_id, coin_pair
                    )
                    notificator(
                        "Buy (market) "
                        + number_for_human(amount_filled)
                        + " "
                        + coin
                        + " at price "
                        + number_for_human(price_buy)
                        + " success"
                    )
                    notificator("Awaiting sell ...")

                    if start_sell_trail_on_sell_signal == "YES":
                        notificator("Awaiting SELL signal ...")
                        if (
                            get_indicators_signal_sell(coin, coin_2, price_buy)[
                                "signal"
                            ]
                            == "SELL"
                        ):
                            trail_sell(
                                coin_pair,
                                buy_order_id,
                                price_buy,
                                coin,
                                coin_2,
                                buy_order,
                                stake_per_trade,
                                coin_pair_for_get_bars,
                            )
                            break

                    trail_sell(
                        coin_pair,
                        buy_order_id,
                        price_buy,
                        coin,
                        coin_2,
                        buy_order,
                        stake_per_trade,
                        coin_pair_for_get_bars,
                    )
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


def trail_sell(
    coin_pair, buy_order_id, price_buy, coin, coin_2, buy_order, stake_per_trade, coin_pair_for_get_bars
):
    try:
        sell_trail_step = float(get_config()["sell_trail_step"])
        start_price = price_buy
        current_price = check_coin_price(coin_pair_for_get_bars)
        current_change_percent = (
            (float(current_price) - start_price) / start_price
        ) * 100
        last_change_percent = current_change_percent

        amount_to_sell = calculate_amount_to_sell(buy_order, coin)

        while True:

            if last_change_percent - sell_trail_step <= current_change_percent:
                if last_change_percent < current_change_percent:
                    last_change_percent = current_change_percent

                current_price = check_coin_price(coin_pair_for_get_bars)
                current_change_percent = (
                    (float(current_price) - start_price) / start_price
                ) * 100

                if debug == "YES":
                    notificator(
                        "last_change_percent :\n"
                        + str(last_change_percent)[:9]
                        + "\n\n"
                        + "current_change_percent :\n"
                        + str(current_change_percent)[:9]
                        + "\n\n"
                        + "sell_trail_step :\n"
                        + str(sell_trail_step)
                    )

                time.sleep(api_requests_frequency)
                if dynamic_trail_enable == "YES":
                    sell_trail_step = dynamic_trail(last_change_percent)
                continue

            else:
                if use_limit_orders == "YES":
                    sell_order_new = make_order(
                        coin_pair, "limit", "sell", amount_to_sell, current_price
                    )
                    sell_order_id = sell_order_new["id"]

                    if check_order_status_by_id(sell_order_id, coin_pair) == "canceled":
                        notificator("Sell order was canceled, restart ...")
                        start_again(coin_pair, coin, coin_2)
                        break

                    if check_order_status_by_id(sell_order_id, coin_pair) == "closed":
                        sell_order = fetch_full_closed_order_by_id(
                            sell_order_id, coin_pair
                        )

                        price_sell = fetch_filled_price_by_id(sell_order_id, coin_pair)
                        amount_filled = fetch_filled_order_amount_by_id(
                            sell_order_id, coin_pair
                        )
                        notificator(
                            "Sell (limit) "
                            + number_for_human(amount_filled)
                            + " "
                            + coin
                            + " at price "
                            + number_for_human(price_sell)
                            + " success"
                        )
                        if get_config()["dynamic_trail_enable"] == "YES":
                            notificator(
                                "Trailing stop was " + number_for_human(sell_trail_step)
                            )

                        trade_result(
                            buy_order_id,
                            sell_order_id,
                            coin_pair,
                            coin_2,
                            sell_order,
                            buy_order,
                            coin,
                            stake_per_trade,
                        )
                        break

                else:
                    sell_order = make_order(
                        coin_pair, "market", "sell", amount_to_sell, None
                    )
                    sell_order_id = sell_order["id"]
                    price_sell = fetch_filled_price_by_id(sell_order_id, coin_pair)
                    amount_filled = fetch_filled_order_amount_by_id(
                        sell_order_id, coin_pair
                    )
                    notificator(
                        "Sell (market) "
                        + number_for_human(amount_filled)
                        + " "
                        + coin
                        + " at price "
                        + number_for_human(price_sell)
                        + " success"
                    )
                    if get_config()["dynamic_trail_enable"] == "YES":
                        notificator(
                            "Trailing stop was " + number_for_human(sell_trail_step)
                        )

                    trade_result(
                        buy_order_id,
                        sell_order_id,
                        coin_pair,
                        coin_2,
                        sell_order,
                        buy_order,
                        coin,
                        stake_per_trade,
                    )
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


def trade_result(
    buy_order_id,
    sell_order_id,
    coin_pair,
    coin_2,
    sell_order,
    buy_order,
    coin,
    stake_per_trade,
):
    try:

        profit_lst = calculate_profit(coin_2)
        notificator(
            "Profit :\n\n"
            + number_for_human(profit_lst[0])
            + " "
            + coin_2
            + "\n"
            + str(profit_lst[2])[:6]
            + " %"
        )

        datetime_start = check_order_date_time_by_id(buy_order_id, coin_pair)
        datetime_end = check_order_date_time_by_id(sell_order_id, coin_pair)

        if save_to_sqlite == "YES":
            save_result_to_sqlite(
                str(sell_order),
                str(buy_order),
                datetime_start,
                datetime_end,
                profit_lst[0],
                str(coin_2),
                str(coin_pair),
            )
        if save_to_firebase == "YES":
            save_result_to_firebase(
                str(sell_order),
                str(buy_order),
                datetime_start,
                datetime_end,
                profit_lst[0],
                str(coin_2),
                str(coin_pair),
            )

        start_again(coin_pair, coin, coin_2)

    except Exception as e:
        if show_error == "YES":
            notificator(str(e))


def start_again(coin_pair, coin, coin_2):

    time.sleep(int(get_config()["common_cooldown_time_sec"]))

    try:
        notificator("Bot id : " + show_bot_id())

        stake_per_trade = get_stake_size(coin_2)

        if use_bnb_for_fee == "YES":
            notificator("We will be use BNB for fee")
            notificator("BNB balance " + str(fetch_balance("BNB")))

        if (
            check_balance_before_start(coin_2, stake_per_trade) is True
            and fetch_ticker(coin_pair) == coin_pair
        ):
            if start_buy_trail_on_buy_signal == "YES":
                notificator("Awaiting for signal from indicators ...")
                if get_indicators_signal(coin, coin_2)["signal"] == "BUY":
                    trail_buy(coin, coin_2, stake_per_trade)
            else:
                trail_buy(coin, coin_2, stake_per_trade)

    except Exception as e:
        if show_error == "YES":
            notificator(str(e))
