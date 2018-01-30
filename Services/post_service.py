"""
@author: Vuong Quoc Viet
@version: 1.0
@since: Jan 20, 2018
"""

import json
from Helpers.posts import fields, header, node, since, until,parameters
from Helpers.utilities import base_url, after
from Models.facebook_post import FacebookPost
from file_service import write
from request_service import request_url

__DATE_SINCE = '2017-01-01'
__DATE_UNTIL = '2017-12-31'


def page_url():
    return base_url() + fields()


def scrape(path, id):
    file_path = path + "/{}.csv".format(id)
    w = write(file_path, header(), 'wb')

    has_next_page = True
    url = base_url() + node(id) + parameters(100) + fields()
    af = ''

    while has_next_page:
        af = '' if af is '' else after(af)
        url_next = url + af + since(__DATE_SINCE) + until(__DATE_UNTIL)
        response = json.load(request_url(url_next))

        if response != '':
            data = response['data']

            for item in data:
                post = FacebookPost(item)
                w.writerow(post.get_info())

            if 'paging' in response:
                af = response['paging']['cursors']['after']
            else:
                has_next_page = False
        else:
            has_next_page = False
