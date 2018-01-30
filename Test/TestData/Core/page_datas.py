import csv
import datetime
import json
import time
from urllib2 import urlopen, Request

from Test.TestData.Core import Token as tk


class PostData:
    def __init__(self, page_id):
        self.__pageId = page_id
        self.__sinceDate = '2017-01-01'
        self.__untilDate = '2017-12-31'
        self.__accessToken = tk().get_token()

    # Get property status
    def get_page_fields(self, _base_url):
        fields = "&fields=message,link,created_time,type,name,id," + \
                 "comments.limit(0).summary(true),shares,reactions" + \
                 ".limit(0).summary(true)"
        return _base_url + fields

    def request_url(self, url):
        req = Request(url)
        success = False
        try:
            response = urlopen(req)

            while success is False:
                try:
                    response = urlopen(req)
                    if response.getcode() == 200:
                        success = True
                        return response.read()

                except Exception as ex:
                    print (ex)
                    time.sleep(2)

                    print ("Error for URL {}: {}".format(url, datetime.datetime.now()))
                    print ("Retrying...")
        except Exception as ex:
            print (ex)
            print ("Error for URL {}: {}".format(url, datetime.datetime.now()))
            pass

    def unicode_encode(self, text):
        return text.encode('utf-8')

    # Get reactions
    def get_reactions(self, baseUrl):
        reaction_types = ['like', 'love', 'wow', 'haha', 'sad', 'angry']
        reactions_dict = {}

        for reaction_type in reaction_types:
            fields = "&fields=reactions.type({}).limit(0).summary(total_count)".format(reaction_type.upper())

            url = baseUrl + fields

            data = json.loads(self.request_url(url))['data']

            data_processed = set()

            for status in data:
                id = status['id']
                count = status['reactions']['summary']['total_count']
                data_processed.add((id, count))

            for id, count in data_processed:
                if id in reactions_dict:
                    reactions_dict[id] = reactions_dict[id] + (count,)
                else:
                    reactions_dict[id] = (count,)

        return reactions_dict

    def process(self, status):

        status_id = status['id']
        status_type = status['type']
        status_message = '' if 'message' not in status else \
            self.unicode_encode(status['message'])
        link_name = '' if 'name' not in status else \
            self.unicode_encode(status['name'])
        status_link = '' if 'link' not in status else \
            self.unicode_encode(status['link'])

        status_published = datetime.datetime.strptime(status['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
        status_published = status_published + datetime.timedelta(hours=7)
        status_published = status_published.strftime('%Y-%m-%d %H:%M:%S')

        num_reactions = 0 if 'reactions' not in status else status['reactions']['summary']['total_count']
        num_comments = 0 if 'comments' not in status else status['comments']['summary']['total_count']
        num_shares = 0 if 'shares' not in status else status['shares']['count']

        return (
        status_id, status_message, link_name, status_type, status_link, status_published, num_reactions, num_comments,
        num_shares)

    def scrape(self):
        with open('DataEx/{}.csv'.format(self.__pageId), 'w') as file:
            w = csv.writer(file)
            w.writerow(["status_id", "status_message", "link_name", "status_type",
                        "status_link", "status_published", "num_reactions",
                        "num_comments", "num_shares", "num_likes", "num_loves",
                        "num_wows", "num_hahas", "num_sads", "num_angrys",
                        "num_special"])

            has_next_page = True
            num_processed = 0
            scrape_starttime = datetime.datetime.now()
            after = ''
            base = "https://graph.facebook.com/v2.11"
            node = "/{}/posts".format(self.__pageId)
            parameters = "/?limit={}&access_token={}".format(100, self.__accessToken)
            since = "&since={}".format(self.__sinceDate) if self.__sinceDate is not '' else ''
            until = "&until={}".format(self.__untilDate) if self.__untilDate is not '' else ''

            print("\t- Scraping {} Facebook Page: {}".format(self.__pageId, scrape_starttime))

            while has_next_page:
                after = '' if after is '' else "&after={}".format(after)
                base_url = base + node + parameters + after + since + until

                url = self.get_page_fields(base_url)
                statuses = json.loads(self.request_url(url))
                reactions = self.get_reactions(base_url)

                for status in statuses['data']:

                    # Ensure it is a status with the expected metadata
                    if 'reactions' in status:
                        status_data = self.process(status)
                        reactions_data = reactions[status_data[0]]

                        # calculate thankful/pride through algebra
                        num_special = status_data[6] - sum(reactions_data)
                        w.writerow(status_data + reactions_data + (num_special,))

                    num_processed += 1
                    if num_processed % 100 == 0:
                        print("\t\t + {} Statuses Processed: {}".format
                              (num_processed, datetime.datetime.now()))

                # if there is no next page, we're done.
                if 'paging' in statuses:
                    after = statuses['paging']['cursors']['after']
                else:
                    has_next_page = False

            print("\t- Done!\n\t * {} Statuses Processed in {}".format(
                num_processed, datetime.datetime.now() - scrape_starttime))
