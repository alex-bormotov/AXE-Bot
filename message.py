import requests
from notification import notificator
from config import get_billig_url


inf_messages = None
messages_url = "/messages"

def info_messages():
    global inf_messages
    try:
        x = requests.get(get_billig_url() + messages_url).json()
        if x == inf_messages:
            pass
        else:
            inf_messages = x

            info = []
            for i in inf_messages["messages"]:
                for k, v in i.items():
                    if k == "info":
                        info.append(v)

            notificator(info[-1:][0]) # first fresh message from db

    except requests.exceptions.RequestException:
        pass
    except Exception :
        pass


def adv_messages():
    try:
        adv_messages = requests.get(get_billig_url() + messages_url).json()
        adv = []
        for i in adv_messages["messages"]:
            for k, v in i.items():
                if k == "adv":
                    adv.append(v)

        notificator(adv[-1:][0]) # first fresh message

    except requests.exceptions.RequestException:
        pass
    except Exception :
        pass
