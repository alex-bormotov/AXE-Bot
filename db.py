from config import get_config
from notification import notificator
import sqlalchemy as db
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as firebase_db

show_error = "YES"

save_to_sqlite = get_config()["save_to_sqlite"]
save_to_firebase = get_config()["save_to_firebase"]

if save_to_sqlite == "YES":
    try:
        engine = db.create_engine("sqlite:///data/trades.sqlite")
        connection = engine.connect()
        metadata = db.MetaData()
        trades = db.Table(
            "trades",
            metadata,
            db.Column("datetime_start", db.String()),
            db.Column("datetime_end", db.String()),
            db.Column("profit_base_currency", db.Float()),
            db.Column("trading_pair", db.String()),
            db.Column("base_currency", db.String()),
            db.Column("unparsed_buy_orders", db.String()),
            db.Column("unparsed_sell_orders", db.String()),
        )
        metadata.create_all(engine)

    except Exception as e:
        if show_error == "YES":
            notificator(str(e))

if save_to_firebase == "YES":
    firebase_credentials_file_name = get_config()["firebase_credentials_file_name"]
    firebase_databaseURL = get_config()["firebase_databaseURL"]
    credentials = credentials.Certificate(firebase_credentials_file_name)
    firebase_admin.initialize_app(credentials, {"databaseURL": firebase_databaseURL})


def save_result_to_sqlite(
    sell_order, buy_order, datetime_start, datetime_end, profit, coin_2, coin_pair
):
    try:
        query = db.insert(trades)
        values_list = [
            {
                "datetime_start": datetime_start,
                "datetime_end": datetime_end,
                "profit_base_currency": profit,
                "trading_pair": coin_pair,
                "base_currency": coin_2,
                "unparsed_buy_orders": buy_order,
                "unparsed_sell_orders": sell_order,
            }
        ]
        ResultProxy = connection.execute(query, values_list)
        notificator("result to db success")

    except Exception as e:
        if show_error == "YES":
            notificator(str(e))


def save_result_to_firebase(
    sell_order, buy_order, datetime_start, datetime_end, profit, coin_2, coin_pair
):
    try:
        db_ref = firebase_db.reference("trades")
        db_ref.push(
            {
                "datetime_start": datetime_start,
                "datetime_end": datetime_end,
                "profit_base_currency": profit,
                "trading_pair": coin_pair,
                "base_currency": coin_2,
                "unparsed_buy_orders": buy_order,
                "unparsed_sell_orders": sell_order,
            }
        )

        notificator("result to firebase success")

    except Exception as e:
        if show_error == "YES":
            notificator(str(e))
