import digikey


class DigikeyAPI:

    def __init__(self, use_api):
        self.use_api = use_api
        digikey.product_details()

    def determent_data(self, data):
        """
        This function will determent if the data received is actually a LCSC data
        :param data: Data found by webcam
        :return: False if not a LCSC data-set
        """

        result = dict()

        # result['type'] = '1D'
        barcode = data['barcode']
        result['result'] = 0
        res = digikey.product_details(barcode)
        print(res)
        if barcode.decode().isdecimal():
            if len(result) > 10:
                result['supplier'] = 'digikey'

        return result

    def search(self, product_info):
        """
        :param product_info:
        :return:
        """

        result = dict()

        return result