"""
@author: Vuong Quoc Viet
@version: 1.0
@since: Jan 20, 2018
"""
from Helpers.utilities import unicode_encode


class FacebookPage:
    def __init__(self, data):
        self.__id = data['id']
        self.__name = unicode_encode(data['name'])
        self.__fanCount = 0 if 'fan_count' not in data else data['fan_count']
        self.__category = " " if 'category' not in data else unicode_encode(data['category'])
        self.__isPublished = False if 'is_published' not in data else data['is_published']

    def get_id(self):
        return self.__id

    def get_info(self):
        info = (self.__id, self.__name, self.__fanCount, self.__category)
        return info

    def is_published(self):
        if self.__isPublished:
            return True
        return False

    def get_fan_count(self):
        return self.__fanCount
