import csv
import datetime
import json
import time
from urllib2 import urlopen, Request

from Test.TestData.Core import PostData
from Test.TestData.Core import Token as tk


class PageData:
    def __init__(self, key_word):
        self.__keyWord = key_word
        self.__accessToken = tk().get_token()

    def get_page_fields(self, _base_url):
        fields = "&fields=id,name,fan_count,is_published"
        return _base_url + fields

    def request_url(self, url):
        req = Request(url)
        success = False
        count = 0

        while success is False:
            try:
                response = urlopen(req)
                if response.getcode() == 200:
                    success = True

            except Exception as ex:
                print (ex)
                time.sleep(2)

                print ("Error for URL {}: {}".format(url, datetime.datetime.now()))
                print ("Retrying...")

            if count == 10:
                break

        return response.read()

    def unicode_encode(self, text):
        return text.encode('utf-8')

    def process(self, page):
        page_id = page['id']
        page_name = self.unicode_encode(page['name'])
        page_fan_count = page['fan_count']
        return (page_id, page_name, page_fan_count)

    def scrape(self):
        with open('DataEx/ListPages_{}.csv'.format(self.__keyWord), 'w') as file:
            w = csv.writer(file)
            w.writerow(["page_id", "page_name", "page_fan_count"])

            has_next_page = True
            number_processed = 0
            scrape_starttime = datetime.datetime.now()
            after = ''
            base = "https://graph.facebook.com/v2.11"
            node = "/search?q={}&type=page".format(self.__keyWord)
            parameters = "&limit={}&access_token={}".format(100, self.__accessToken)

            print("Start: {}".format(scrape_starttime))

            while has_next_page or number_processed <= 10000:
                after = '' if after is '' else '&after={}'.format(after)

                url_next = base + node + parameters + after
                url = self.get_page_fields(url_next)
                page_information = json.loads(self.request_url(url))

                for info in page_information['data']:
                    fan_count = 0 if 'fan_count' not in info else info['fan_count']
                    is_published = False if 'is_published' not in info else info['is_published']
                    if fan_count >= 10000 and is_published:
                        page_data = self.process(info)
                        w.writerow(page_data)
                        PostData(info['id']).scrape()

                        number_processed += 1
                        if number_processed % 100 == 0:
                            print("{} Page Processed: {}".format(number_processed, datetime.datetime.now()))

                # if there is no next page, we're done.
                if 'paging' in page_information:
                    after = page_information['paging']['cursors']['after']
                else:
                    has_next_page = False

            print("\nDone!\n{} Page Processed in {}".format(
                number_processed, datetime.datetime.now() - scrape_starttime))
