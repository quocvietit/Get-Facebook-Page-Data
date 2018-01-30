"""
@author: Vuong Quoc Viet
@version: 1.0
@since: Jan 20, 2018
"""

__NODE = "/search?q={}&type=page"
__FIELDS = "&fields=id,name,fan_count,is_published,category"
__HEADER = ["id", "name", "fan_count", "category"]


def fields():
    return __FIELDS


def header():
    return __HEADER


def node(keyword):
    return __NODE.format(keyword)
