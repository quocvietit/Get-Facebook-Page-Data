"""
@author: Vuong Quoc Viet
@version: 1.0
@since: Jan 20, 2018
"""
from Core.token import token

__NODE = "/{}/posts"
__FIELDS = "&fields=message,link,created_time,type,name,id," + \
           "comments.limit(0).summary(true),shares,reactions" + \
           ".limit(0).summary(true)"
__REACTION_FIELDS = "&fields=reactions.type({}).limit(0).summary(total_count)"
__HEADER = ["id", "essage", "name", "type",
            "link", "published", "reactions",
            "comments", "shares"]
__REACTION_TYPES = ['like', 'love', 'wow', 'haha', 'sad', 'angry']
__SINCE = "&since={}"
__UNTIL = "&until={}"
__PARAMETERS = "/?limit={}&access_token={}"
__ACCESS_TOKEN = token()


def fields():
    return __FIELDS


def reaction_fields():
    return __REACTION_FIELDS


def header():
    return __HEADER


def node(id):
    return __NODE.format(id)


def since(date=''):
    return __SINCE.format(date) if date is not '' else ''


def until(date=''):
    return __UNTIL.format(date) if date is not '' else ''


def parameters(limit):
    return __PARAMETERS.format(limit, __ACCESS_TOKEN)
