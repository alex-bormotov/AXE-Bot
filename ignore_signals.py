import time
from time import sleep
from notification import notificator
from config import get_config


ignore_buy_signal_counter = 0
ignore_sell_signal_counter = 0


def ignore_buy_signal_times(signal, times):

    global ignore_buy_signal_counter

    if signal["signal"] == "BUY" and ignore_buy_signal_counter < times:
        notificator(
            "Ignore {} {} ... cooldown {} seconds".format(
                signal["signal"],
                str(ignore_buy_signal_counter + 1),
                get_config()["ignore_buy_cooldown_sec"],
            )
        )
        ignore_buy_signal_counter = ignore_buy_signal_counter + 1
        time.sleep(int(get_config()["ignore_buy_cooldown_sec"]))
        return "PASS"
    else:
        notificator("Execute {}".format(signal["signal"]))
        ignore_buy_signal_counter = 0
        return "OK"


def ignore_sell_signal_times(signal, times):

    global ignore_sell_signal_counter

    if signal["signal"] == "SELL" and ignore_sell_signal_counter < times:
        notificator(
            "Ignore {} {} ... cooldown {} seconds".format(
                signal["signal"],
                str(ignore_sell_signal_counter + 1),
                get_config()["ignore_sell_cooldown_sec"],
            )
        )
        ignore_sell_signal_counter = ignore_sell_signal_counter + 1
        time.sleep(int(get_config()["ignore_sell_cooldown_sec"]))
        return "PASS"
    else:
        notificator("Execute {}".format(signal["signal"]))
        ignore_sell_signal_counter = 0
        return "OK"


def ingnore_signal_time(signal, time_sec):

    notificator(
        "{} signal received, sleep {} sec ...".format(signal["signal"], time_sec)
    )
    time.sleep(time_sec)
    notificator("Execute {}, after sleep {} sec ".format(signal["signal"], time_sec))
    return signal
