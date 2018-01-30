"""
@author: Vuong Quoc Viet
@version: 1.0
@since: Jan 20, 2018
"""

import json
import threading
from Helpers.pages import fields, header, node
from Helpers.utilities import base_url, parameters, after
from Models.facebook_page import FacebookPage
from file_service import write
from request_service import request_url
from post_service import scrape as scrape_post


def page_url():
    return base_url() + fields()


def scrape(path, keyword):
    file_path = path + "/Pages.csv"
    w = write(file_path, header(), "ab")

    has_next_page = True
    number_processed = 0
    url = base_url() + node(keyword) + parameters(100) + fields()
    af = ''

    while has_next_page:
        af = '' if af is '' else after(af)
        url_next = url + af
        response = json.load(request_url(url_next))

        if response != '':
            data = response['data']

            for item in data:
                page = FacebookPage(item)
                if page.is_published() and page.get_fan_count() > 1000:
                    page_info = page.get_info()
                    w.writerow(page_info)

                    try:
                        post = threading.Thread(target=scrape_post(path, page.get_id()), args=())
                        post.start()
                    except:
                        print "Not crape {}".format(page.get_id())

                    number_processed += 1

            if 'paging' in response:
                af = response['paging']['cursors']['after']
            else:
                has_next_page = False
        else:
            has_next_page = False

    return number_processed
