# coding=utf-8
"""
@author: Vuong Quoc Viet
@version: 1.0
@since: Jan 20, 2018
"""
import os
import datetime
from Services.page_service import scrape

__PATH = "../Data"


def get_data(list_keyword):
    start_time = datetime.datetime.now()
    print("Start: {}".format(start_time))

    number_page = get_pages(list_keyword)

    end_time = datetime.datetime.now()
    print "Done\n Find {} page in {}".format(number_page, end_time - start_time)


def get_pages(list_keyword):
    number_page = 0
    for keyword in list_keyword:
        print "Scrape {} ...".format(keyword)
        number = scrape(__PATH, keyword)
        print "Done \n Find {} with keyword: {}".format(number, keyword)
        number_page += number
    return number_page


if __name__ == "__main__":
    keywords = {#"tintuc",
                #"tin+tức+viêt+nam",
                #"thời+sự",
                "các+trang+báo"}
                #"tin+nhanh",
                #"báo",
                #"báo+mới",
                #"trang+tin+tức",
                #"trang+báo",
                #"trang+tin+tức+hàng+ngày",
                #"trang+tin+tức+mỗi+ngày",
                #"tin+tức+trong+nước",
                #"tin+mới"}

    get_data(keywords)
