"""
@author: Vuong Quoc Viet
@version: 1.0
@since: Jan 20, 2018
"""

import csv


def write(file_path, header, handle):
    try:
        f = open(file_path, handle)
        w = csv.writer(f, header)
        return w

    except Exception as ex:
        print ex
