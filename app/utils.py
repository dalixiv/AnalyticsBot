import re

import requests
import json

# todo: move to config
URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'


def load_exchange():
    return json.loads(requests.get(URL).text)


def get_exchange(ccy_key):
    for exc in load_exchange():
        if ccy_key == exc['ccy']:
            return exc
    return False


# fixme: implement or delete this function
def get_exchanges(ccy_pattern):
    result = []
    ccy_pattern = re.escape(ccy_pattern) + '.*'
    # for exc in load_exchange():
    #    if re.match(ccy_pattern, exc['ccy'], re.IGNORECASE) is not None:
    #        result.append(exc)
    #        return result


def serialize_ex(ex_json, diff=None):
    result = (
            "<b>"
            + ex_json["base_ccy"]
            + " -> "
            + ex_json["ccy"]
            + ":</b>\n\n"
            + "Buy: "
            + ex_json["buy"]
    )
    if diff:
        result += (
                " "
                + serialize_exchange_diff(diff["buy_diff"])
                + "\n"
                + "Sell: "
                + ex_json["sale"]
                + " "
                + serialize_exchange_diff(diff["sale_diff"])
                + "\n"
        )
    else:
        result += "\nSell: " + ex_json["sale"] + "\n"
    return result


def serialize_exchange_diff(diff):
    result = ""
    if diff > 0:
        result = (
                "("
                + str(diff)
        )
    elif diff < 0:
        result = (
                "("
                + str(diff)[1:]
        )
    return result
