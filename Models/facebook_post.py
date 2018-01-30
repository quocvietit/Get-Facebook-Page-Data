"""
@author: Vuong Quoc Viet
@version: 1.0
@since: Jan 20, 2018
"""
import datetime
from Helpers.utilities import unicode_encode


class FacebookPost:
    def __init__(self, data):
        self.__id = unicode_encode(data['id'])
        self.__type = unicode_encode(data['type'])
        self.__message = '' if 'message' not in data else unicode_encode(data['message'])
        self.__linkName = '' if 'name' not in data else unicode_encode(data['name'])
        self.__statusName = '' if 'link' not in data else data['link']
        self.__statusPublished = datetime.datetime.strptime(data['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
        self.__statusPublished = self.__statusPublished + datetime.timedelta(hours=7)
        self.__statusPublished = self.__statusPublished.strftime('%Y-%m-%d %H:%M:%S')
        self.__numberReactions = 0 if 'reactions' not in data else data['reactions']['summary']['total_count']
        self.__numberComments = 0 if 'comments' not in data else data['comments']['summary']['total_count']
        self.__numberShares = 0 if 'shares' not in data else data['shares']['count']

    def get_info(self):
        info = (self.__id,
                self.__type,
                self.__message,
                self.__linkName,
                self.__statusName,
                self.__statusPublished,
                self.__numberReactions,
                self.__numberComments,
                self.__numberShares)
        return info
