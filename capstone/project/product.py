import json


class Product:

    def __init__(self):
        self.data_file = 'products.json'

    def get_all(self):
        """ Extract only the data we want to work with from the json file. """

        with open(self.data_file) as data:
            data = json.load(data)

        products = []
        for product in data:
            products.append({
                'id': product['product_id'],
                'full_name': product['full_product_name'],
                'short_name': product['short_product_name'],
                'overview': product['overview'],
                'specification': product['specification'],
                'meta_keyword': product['meta_keyword'],
                'meta_description': product['meta_description'],
                'price': product['retail_price'],
                'related': product['related_products']
            })

        return products

    def find_by_id(self, product_id):
        """
        Find an item by the product id, filter will return a
        list so return the first item that matches only.
        """

        return list(filter(lambda product: product['id'] == product_id, self.get_all()))[0]
