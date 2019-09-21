import datetime as dt
import time
import hashlib
import json
import requests
from config import get_config, write_config
from notification import notificator
from time import sleep
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from config import get_billig_url
from secrets import token_urlsafe


licence_hash = None
ecnrypted_licence_time = None

secret_key_for_hashing = "xsCsW1uHZN_KdrQSr-U9q7rgO0q0gpWY0RH10lcCJQ4="
secret_for_encruption_licence_time = "CAQRzbEvyDxfy-h3Nk-fURRWlzuzneygxSCMLfv2vsY="
# salt = secret_key_for_hashing - mean salt for hashing get_config()["key"]
# key = secret_for_encruption_licence_time + show_bot_id() - mean key for encrypt licence_time
######################################################################################################################
# It is for generate time on billing server
def encrypt_licence_time_decoded():

    x = dt.datetime.utcnow() + timedelta(1 * 365 / 12)  # 1 Month
    # x = datetime.utcnow() + timedelta(minutes=1)
    x = str(x)
    x = x.encode()

    key = secret_for_encruption_licence_time + show_bot_id()

    f = Fernet(key)
    encrypt_value = f.encrypt(x)
    encrypt_value = encrypt_value.decode()

    return encrypt_value


# It is for generate time on billing server
###########################################################
###########################################################
def hash_licence():

    salt = secret_key_for_hashing
    licence_hash = (
        hashlib.sha256(salt.encode() + get_config()["key"].encode()).hexdigest()
        + ":"
        + salt
    )
    return licence_hash


def write_bot_hash_if_null():

    secret_for_write_hash = "K_z1Lter7c-33tr76jUujXEqIU12uP1UsAYAcyPgZ5A="

    billing_api_url = get_billig_url()
    billing_api_write_licence_url = "/updatehash"
    endpoint_for_write_bot_hash = billing_api_url + billing_api_write_licence_url

    if login_on_billing() == {'message': "User {} doesn't exist".format(show_bot_id())}:
        auth_token_access = registration_on_billing()["access_token"]
    else:
        auth_token_access = login_on_billing()["access_token"]


    auth_token_access_bearer = "Bearer " + auth_token_access
    headers_access = {"Authorization": auth_token_access_bearer}
    bot_hash_dict = {"bot_id": show_bot_id(), "bot_hash": hash_licence(), "secret_for_write_hash": secret_for_write_hash}


    requests.post(endpoint_for_write_bot_hash, json=bot_hash_dict, headers=headers_access, verify=True).json()

def show_bot_id():
    try:
        bot_id = get_config()["bot_id"]

    except Exception:
        config = get_config()
        config.update({"bot_id": token_urlsafe(7)})
        write_config(config)
        bot_id = get_config()["bot_id"]

    return bot_id


def check_licence_hash():

    global licence_hash

    if licence_hash == None:
        licence_hash = hash_licence()
        password, salt = licence_hash.split(":")
        return (
            password
            == hashlib.sha256(salt.encode() + get_config()["key"].encode()).hexdigest()
        )
    else:
        password, salt = licence_hash.split(":")
        return (
            password
            == hashlib.sha256(salt.encode() + get_config()["key"].encode()).hexdigest()
        )

def compare_licence_hashes_is_same():
    billing_api_url = get_billig_url()
    billing_api_licence_url = "/licence/"
    endpoint_for_get_licence_time = billing_api_url + billing_api_licence_url + show_bot_id()

    if login_on_billing() == {'message': "User {} doesn't exist".format(show_bot_id())}:
        auth_token_access = registration_on_billing()["access_token"]
    else:
        auth_token_access = login_on_billing()["access_token"]

    auth_token_access_bearer = "Bearer " + auth_token_access
    headers_access = {"Authorization": auth_token_access_bearer}

    bot_hash_dict = requests.get(endpoint_for_get_licence_time, headers=headers_access, verify=True).json()
    bot_hash_on_billing = bot_hash_dict["users"][0]["bot_hash"]

    if bot_hash_on_billing == None:
        write_bot_hash_if_null()
        bot_hash_dict = requests.get(endpoint_for_get_licence_time, headers=headers_access, verify=True).json()
        bot_hash_on_billing = bot_hash_dict["users"][0]["bot_hash"]

    if hash_licence() != bot_hash_on_billing:
        return False
    else:
        return True
###########################################################

def registration_on_billing():

    secret_for_bot_registration = "LXORWIiKFXUSBO2Ip_sVKpRByuwDVhSOt9nTgopUoQ8="

    billing_api_url = get_billig_url()
    billing_api_registration_url = "/registration"
    endpoint_for_registration = billing_api_url + billing_api_registration_url
    registration_data_json = { "bot_id": show_bot_id(), "bot_hash": hash_licence(), "secret_for_bot_registration": secret_for_bot_registration}

    server_answer = requests.post(endpoint_for_registration, json=registration_data_json, verify=True).json()

    return server_answer


def login_on_billing():

    secret_for_bot_login = "Jrp-_Xipu6xFdYrp_9RDK5Ur3wDUI16J0nc0spbRvE0="

    billing_api_url = get_billig_url()
    billing_api_login_url = "/botlogin"
    endpoint_for_login = billing_api_url + billing_api_login_url
    login_data_json = {"bot_id": show_bot_id(), "secret_for_bot_login": secret_for_bot_login}

    server_answer = requests.post(endpoint_for_login, json=login_data_json, verify=True).json()

    return server_answer


def get_encrypted_licence_time(auth_token_access):

    billing_api_url = get_billig_url()
    billing_api_licence_url = "/licence/"
    endpoint_for_get_licence_time = billing_api_url + billing_api_licence_url + show_bot_id()

    auth_token_access_bearer = "Bearer " + auth_token_access
    headers_access = {"Authorization": auth_token_access_bearer}

    bot_licence = requests.get(endpoint_for_get_licence_time, headers=headers_access, verify=True).json()
    ecnrypted_licence_time = bot_licence["users"][0]["bot_licence"]

    if ecnrypted_licence_time == None:
        return "Null"
    else:
        key = secret_for_encruption_licence_time + show_bot_id()
        f = Fernet(key)
        ecnrypted_licence_time = ecnrypted_licence_time.encode()
        x = f.decrypt(ecnrypted_licence_time)
        x = x.decode()
        return x


def decrypt_licence_time():

    try:
        if login_on_billing() == {'message': "User {} doesn't exist".format(show_bot_id())}:
            auth_token_access = registration_on_billing()["access_token"]
            ecnrypted_licence_time = get_encrypted_licence_time(auth_token_access)
            return ecnrypted_licence_time
        else:
            auth_token_access = login_on_billing()["access_token"]
            ecnrypted_licence_time = get_encrypted_licence_time(auth_token_access)
            return ecnrypted_licence_time

    except requests.exceptions.RequestException as e:
        return "Null"



def check_licence_is_expire():

    return False

    # if compare_licence_hashes_is_same() == False or decrypt_licence_time() == "Null":
    #     return True
    # else:
    #     if dt.datetime.utcnow() > dt.datetime.fromisoformat(decrypt_licence_time()):
    #         return True
    #     else:
    #         return False
