import json
import sys
import requests

show_error = "YES"


def get_config():
    with open("config/config.json", "r") as read_file:
        config = json.load(read_file)
        return config


def write_config(config):
    with open("config/config.json", "w") as write_file:
        json.dump(config, write_file, indent=1)


def check_config_error():
    for k, v in get_config().items():
        if v == "":
            print(str(k) + " <------> is blank, fix it")
            sys.exit()
        if type(v) != str:
            print(str(k) + ' <------> is not in a "", fix it')
            sys.exit()

    if get_config()["exchange_for_trade"] != "binance":
        print("Currently supports Binance only")
        sys.exit()
    if get_config()["exchange_for_trade"] == "binance":
        if (
            get_config()["coin_2"]
            not in "BTC, ETH, BNB, XRP, USDT, TUSD, PAX, USDS, USDC"
        ):
            print("Wrong base currency (coin_2)")
            sys.exit()


def get_billig_url():
    url_1 = "https://axe-bill-app.axe-dev.com"
    url_2 = "https://axe-bill-app.herokuapp.com"

    try:
        if requests.get(url_1).status_code == 200:
            billing_api_url = url_1
            return billing_api_url

    except requests.exceptions.RequestException:
        if requests.get(url_2).status_code == 200:
            billing_api_url = url_2
            return billing_api_url
