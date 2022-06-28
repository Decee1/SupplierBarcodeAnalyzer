"""
This function tests the getparts function and ensures it deliveres the correct result by using
a data_set of collected data from QR codes, barcodes and so on users have collected
"""
import ast
from json import loads
from types import SimpleNamespace

import getparts

f = open('data_set.txt', 'r')
data_set = f.readlines()

api = getparts.API(cred=None, debug=False, use_api=False)

for data in data_set:
    data = data.replace("\n", "")
    print(data)
    data_list = eval(data)
    supplier = data_list[0]
    barcode = data_list[1]

    print(f"Testing.. expect {supplier} from {barcode}")
    data = SimpleNamespace()
    data.data = barcode

    result = api.search(data)
    print(result)

    if supplier in result['supplier']:
        print("Received correct supplier")



