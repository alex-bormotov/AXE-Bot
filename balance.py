import ccxt
from exchange import exchange
from notification import notificator
from config import get_config
from human import number_for_human
from demo import demo_or_full
from licence import check_licence_is_expire
from message import adv_messages


show_error = "YES"
exchange = exchange()
minimal_order_size_btc = 0.001
minimal_order_size_eth = 0.01
minimal_order_size_bnb = 0.1
minimal_order_size_xrp = 10
minimal_order_size_usd_x = 10
USD_X = "USDT, TUSD, PAX, USDS, USDC"


def get_stake_size(coin_2):

    if get_config()["use_all_balance"] == "YES":
        notificator("We will use all " + str(coin_2) + " balance for trade")
        return demo_or_full(fetch_balance(coin_2), coin_2)
    else:
        return demo_or_full(float(get_config()["stake_per_trade"]), coin_2)


def check_balance_before_start(coin, stake_per_trade):
    balance = fetch_balance(coin)
    if balance >= stake_per_trade and minimum_order_size(coin, stake_per_trade) is True:
        if check_licence_is_expire():
            adv_messages()
        notificator("You have " + number_for_human(balance) + " " + str(coin))
        notificator(
            "Stake will be " + number_for_human(stake_per_trade) + " " + str(coin)
        )
        notificator("We will trade :")
        return True

    else:
        if check_licence_is_expire():
            adv_messages()
        notificator("You have " + number_for_human(balance) + " " + str(coin))
        notificator("Stake " + number_for_human(stake_per_trade) + " " + str(coin))
        notificator("Small " + str(coin) + " balance !")
        notificator("Bot stopped")
        return False


def fetch_balance(coin):
    try:
        balance = exchange.fetch_balance()
        balance = balance[coin]["free"]
        return balance

    except ccxt.NetworkError as e:
        if show_error == "YES":
            notificator(str(e))
    except ccxt.ExchangeError as e:
        if show_error == "YES":
            notificator(str(e))
    except Exception as e:
        if show_error == "YES":
            notificator(str(e))


def minimum_order_size(coin, stake_per_trade):
    if coin == "BTC":
        if minimal_order_size_btc > stake_per_trade:
            notificator(
                "Minimal order size " + str(minimal_order_size_btc) + " " + coin
            )
            return False
        else:
            return True

    if coin == "ETH":
        if minimal_order_size_eth > stake_per_trade:
            notificator(
                "Minimal order size " + str(minimal_order_size_eth) + " " + coin
            )
            return False
        else:
            return True

    if coin == "BNB":
        if minimal_order_size_bnb > stake_per_trade:
            notificator(
                "Minimal order size " + str(minimal_order_size_bnb) + " " + coin
            )
            return False
        else:
            return True

    if coin == "XRP":
        if minimal_order_size_xrp > stake_per_trade:
            notificator(
                "Minimal order size " + str(minimal_order_size_xrp) + " " + coin
            )
            return False
        else:
            return True

    if coin in USD_X:
        if minimal_order_size_usd_x > stake_per_trade:
            notificator(
                "Minimal order size " + str(minimal_order_size_usd_x) + " " + coin
            )
            return False
        else:
            return True
