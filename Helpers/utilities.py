"""
@author: Vuong Quoc Viet
@version: 1.0
@since: Jan 20, 2018
"""

from Core.token import token

__BASE_URL = "https://graph.facebook.com/v2.11"
__PARAMETERS = "&limit={}&access_token={}"
__AFTER = '&after={}'
__ACCESS_TOKEN = token()


def unicode_encode(text):
    return text.encode("utf-8")


def base_url():
    return __BASE_URL


def parameters(limit):
    return __PARAMETERS.format(limit, __ACCESS_TOKEN)


def after(url):
    return __AFTER.format(url)
