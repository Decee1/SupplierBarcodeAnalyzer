from types import SimpleNamespace


class LcscAPI():

    def __init__(self, use_api):
        self.use_api = use_api

    def determent_data(self, recv_data):
        """
        This function will determent if the data received is actually a LCSC data
        :param recv_data: Data found by webcam
        :return: False if not a LCSC data-set
        """

        # Example of data received from QRlabel
        # {pbn:PICK211019100003,on:SO2110190475,pc:C393099,pm:RLM10JTSMR010,qty:100,mc:,cc:1,pdi:48666438,hp:0}
        # The data in the barcode label is X48666438
        data = recv_data['barcode'].decode()
        data_dict = dict()
        result = dict()
        result['result'] = 0

        #if 'QRCODE' in recv_data['type']:
        try:
            data = data.replace("{", "")
            data = data.replace("}", "")

            data_split = data.split(",")

            for sub_data in data_split:
                sub_data = sub_data.split(":")
                data_dict[sub_data[0]] = sub_data[1]

            result['type'] = '2D'
            result['manufacturerPN'] = data_dict['pm']
            result['quantity'] = data_dict['qty']
            result['supplierPN'] = data_dict['pc']
            result['supplier'] = 'lcsc'
            result['result'] = 1
            print("LCSC component FOUND")
        except Exception as e:
            print(f"LCSC check failed: {e}")
            result['result'] = 0
        # else:
        #   # Does not match any LCSC label types
        #    result['result'] = 0
        return result

    def search(self, product_info):
        """
        This function converts the product info into data
        :param product_info:
        :return:
        """

        result = dict()

        # class lcsc:
        def lcsc_scrape(pn):
            lcscPN = pn
            print(f"LCSC PN: {pn}")

            # create an HTML Session object
            session = HTMLSession()

            # Use the object above to connect to needed webpage
            r1 = session.get("https://lcsc.com/search?q=" + lcscPN)
            print(r1)
            # Run any JavaScript code on webpage
            r1.html.render()
            print("here")

            # Find absolute link for product page
            a = r1.html.find(
                'body > div#lcsc.push-body > div#global_search.contianer > div.table-content > section > div > div#product_table_list > div.product-list-area.table-area > table')
            print(a)
            links = a[0].absolute_links
            print(links)
            product_page = ""
            for link in links:
                if lcscPN + '.html' in link:
                    product_page = link

            # Load product page

            direct = session.get(product_page)
            print(direct)
            soup = BeautifulSoup(direct.html.html, "lxml")
            print(soup)
            # Find correct product table
            table = soup.find('table', attrs={'class': 'products-specifications'})  # 2nd table
            print(table)
            table_body = table.find('tbody')
            print(table_body)
            rows = table_body.find_all('tr')
            result = lcscdata({})
            print(result)
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                line = [ele for ele in cols if ele]
                try:
                    result.value.update({line[0]: line[1]})
                except:
                    pass
            return result

        return result