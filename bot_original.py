import time
from time import sleep
from datetime import datetime
from config import (
    get_config,
    check_config_error
)
from balance import check_balance_before_start, fetch_balance, get_stake_size
from notification import notificator
from trader import trail_buy
from error_handling import fetch_ticker
from indicators import get_indicators_signal
from licence import show_bot_id, registration_on_billing
from message import info_messages

show_error = "YES"

check_config_error()

registration_on_billing()

info_messages()

coin = get_config()["coin"].upper()
coin_2 = get_config()["coin_2"].upper()

use_bnb_for_fee = get_config()["use_bnb_for_fee"]

start_buy_trail_on_buy_signal = get_config()["start_buy_trail_on_buy_signal"]

notificator("Bot id : " + show_bot_id())

stake_per_trade = get_stake_size(coin_2)


if use_bnb_for_fee == "YES":
    notificator("We will be use BNB for fee")
    notificator("BNB balance " + str(fetch_balance("BNB")))


def main():

    coin_pair = coin + "/" + coin_2

    try:
        balance_coin_2_is_enough = check_balance_before_start(
            coin_2, stake_per_trade
        )
        if balance_coin_2_is_enough == True:

            tiker = fetch_ticker(coin_pair)
            if tiker == coin_pair:

                if start_buy_trail_on_buy_signal == "YES":
                    notificator("Awaiting for signal from indicators ...")
                    if get_indicators_signal(coin, coin_2)["signal"] == "BUY":
                        trail_buy(coin, coin_2, stake_per_trade)
                else:
                    trail_buy(coin, coin_2, stake_per_trade)

    except Exception as e:
        if show_error == "YES":
            notificator(str(e))



if __name__ == "__main__":
    main()
