# import mouser.cli as mouser  # mouser.mouser_cli()


class MouserAPI():

    def __init__(self, use_api):
        self.use_api = use_api

        pass

    def determent_data(self, data):
        """
        This function will determent if the data received is actually a Mouser data
        :param data: Data found by webcam
        :return: False if not a Mouser data-set
        """
        # b'>[)>06\x1dK22870336\x1d14K001\x1d1PATSAMD21G18A-AU\x1dQ25\x1d11K064227427\x1d4LTH\x1d1VMicrochip'
        result = dict()
        result['result'] = 0

        try:
            decoded_data = data["barcode"].decode()

            # ['>[)>06', 'K22870336', '14K001', '1PATSAMD21G18A-AU', 'Q25', '11K064227427', '4LTH', '1VMicrochip']
            data_lst = decoded_data.split()

            # result['type'] = '1D'
            if ">[)>06" in data_lst:
                result['type'] = 'QRCODE'
                result['supplier'] = 'mouser'
                result["result"] = 1
                result['manufacturerPN'] = data_lst[3].replace("1P", "")
                result['manufacturerName'] = data_lst[7].replace("1V", "")
                result['quantity'] = data_lst[4].replace("Q", "")
                result['supplierPN'] = "" # data_dict['pc']

            return result

        except:
            pass

        return result

    def scan(self, data):
        """
        This function will determent if the data received is actually a LCSC data
        :param data: Data found by webcam
        :return: False if not a LCSC data-set
        """

        result = dict()

        return result

    def search(self, product_info):
        """
        :param product_info:
        :return:
        """

        result = dict()

        return result
