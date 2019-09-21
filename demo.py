import sys
from notification import notificator
from licence import check_licence_is_expire

show_error = "YES"

def demo_or_full(stake_per_trade, coin_2):

    #return stake_per_trade

    stake_demo_btc = 0.03

    demo_message = (
        "This is DEMO edition :(\n\nLimit for trading "
        + str(stake_demo_btc)
        + " BTC "
        + "\n\n"
        + "In DEMO allowed trading with BTC only"
        + "\n\n"
        + "For get more trade limit and trade other pairs, please, buy Full edition :)"
        + "\n\n"
        + "https://axe-bot.com"
    )

    try:
        if (
            coin_2 == "BTC"
            and stake_per_trade > stake_demo_btc
            and check_licence_is_expire() == True
        ):
            notificator(demo_message)
            return stake_demo_btc

        if (
            coin_2 in "ETH, BNB, XRP, USDT, TUSD, PAX, USDS, USDC"
            and check_licence_is_expire() == True
        ):
            notificator(demo_message)
            sys.exit()

        else:
            return stake_per_trade


    except Exception as e:
        if show_error == "YES":
            notificator(str(e))
