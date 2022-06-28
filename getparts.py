"""
Python3

API tool for electronic component suppliers (digikey, mouser, LCSC)
https://github.com/maholli/getparts
M.Holliday
"""

import os

import configparser

from lcsc_API import LcscAPI
from digikey_API import DigikeyAPI
from mouser_API import MouserAPI


def printlevel(level, text):
    print('\t' * level + str(text))


class API:
    RECORDS_FILE = 'api_records_digi.txt'

    def __init__(self, cred=None, debug=False, use_api=True):

        self.DEBUG = debug
        self.use_api = use_api

        if cred is None:
            print("Cred argument is not specified, loading from config.ini")
            filename = 'config.ini'
            config = configparser.ConfigParser()
            config.read(filename)

            if 'digikey' in config and 'DIGIKEY_CLIENT_ID' in config['digikey']:
                config.read(filename)
                print(f"Passing data from {filename}")
                os.environ['DIGIKEY_CLIENT_ID'] = config['digikey']['DIGIKEY_CLIENT_ID']
                os.environ['DIGIKEY_CLIENT_SECRET'] = config['digikey']['DIGIKEY_CLIENT_SECRET']
                os.environ['DIGIKEY_STORAGE_PATH'] = config['digikey']['DIGIKEY_STORAGE_PATH']


                os.environ['MOUSER_ORDER_API_KEY'] = config['mouser']['client_id']
                os.environ['MOUSER_PART_API_KEY'] = ""

            else:
                print("Missing config.ini file, creating file")

                # Create config file
                config['digikey'] = dict()
                config['digikey']['DIGIKEY_CLIENT_ID'] = ""
                config['digikey']['DIGIKEY_CLIENT_SECRET'] = ""
                config['digikey']['DIGIKEY_STORAGE_PATH'] = ""

                config['mouser'] = dict()
                config['mouser']['client_id'] = ""
                config['mouser']['client_secret'] = ""
                config['mouser']['mouser_key'] = ""

                with open(filename, "w") as fp:
                    config.write(fp)

                exit("Please go and configure the config.ini file")

        self.LcscAPI = LcscAPI(use_api=use_api)
        self.MouserAPI = MouserAPI(use_api=use_api)
        self.DigikeyAPI = DigikeyAPI(use_api=use_api)

        self.compare_name = "comp"

    def search(self, data):
        """
        Determent the correct result by using each API in the system to return a value between 0 and 1
        Then check which one is closest to one, each API will check different aspect from the value to match it's
        Expected result and from there give a score/percentage that it thinks the value come from
        :param data:
        :return:
        """
        print(data)
        result = dict()
        result["barcode"] = data.data
        if hasattr(result, "type"):
            result["type"] = data.type

        compare_name = self.compare_name

        # Stores the results from each test
        result[compare_name] = dict()

        print("Testing LCSC")
        res = self.LcscAPI.determent_data(result)
        result[compare_name]["lcsc"] = dict()
        result[compare_name]["lcsc"].update(res)

        print("Testing Digikey")
        res = self.DigikeyAPI.determent_data(result)
        result[compare_name]["digikey"] = dict()
        result[compare_name]["digikey"].update(res)

        print("Testing Mouser")
        res = self.MouserAPI.determent_data(result)
        result[compare_name]["mouser"] = dict()
        result[compare_name]["mouser"].update(res)

        collect_data(result)

        res = self._compare_data(result)

        return res

    def _compare_data(self, data_dict):
        """
        This function will compare each result received from each API and find the one that is closest to 1
        :param data_dict:
        :return:
        """

        lowest_val = dict()
        lowest_val["API"] = ""
        lowest_val["perc"] = 0
        for data in data_dict[self.compare_name]:
            data = data_dict[self.compare_name][data]
            if data["result"] > lowest_val["perc"]:
                lowest_val["perc"] = data["result"]
                lowest_val["API"] = data["supplier"]

        print(f"The closest value from APIs: {lowest_val['API']}")

        return data_dict[self.compare_name][lowest_val["API"]]

def collect_data(data):
    """
    Collect all data received and put in into a file to be evaluated/analyzed for testing/simulation of library
    :param data:
    :return:
    """
    barcode = data["barcode"]
    supplier = ""

    # if supplier is not in data, don't log data
    if "supplier" not in data:
        return 0

    collected_set_filename = 'data_collected.txt'
    if not os.path.isfile(collected_set_filename):
        open(collected_set_filename, 'a').close()  # Creates the file

    f = open(collected_set_filename, 'a')
    print(f"Adding result to {collected_set_filename}")
    f.write(f'[{supplier}, {barcode}]\n')
    f.close()

    data_set_filename = 'data_set.txt'
    if not os.path.isfile(data_set_filename):
        open(data_set_filename, 'a').close()  # Creates the file

    f = open(data_set_filename, 'r')
    data_write = f"['{supplier}',{barcode}]\n"
    if data_write not in f.readlines():
        print(f"Adding '[{supplier}, {barcode}]' to data_set")
        f = open(data_set_filename, 'a')
        f.write(data_write)
        f.close()


class lcscdata:

    def __init__(self, val):
        self.value = val

    def json(self):
        return self.value
