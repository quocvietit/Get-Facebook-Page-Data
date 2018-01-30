"""
@author: Vuong Quoc Viet
@version: 1.0
@since: Jan 20, 2018
"""

from urllib2 import urlopen, Request
import time


# request url and return data
def request_url(url):
    req = Request(url)
    success = False
    count = 0

    while success is False or count < 10:
        try:
            response = urlopen(req)
            if response.getcode() == 200:
                success = True
                return response
        except Exception as ex:
            print ex
            time.sleep(2)

        count = count + 1

    return ''
