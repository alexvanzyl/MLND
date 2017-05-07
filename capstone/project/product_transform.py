from bs4 import BeautifulSoup as bs


class Transform:
    """
    The product transformer allows us to easily get any key from a the product dict
    and parse the output either as raw html, prettified html or just plain text.
    """

    def __init__(self, product):
        """
        :param product: The product dict to transform.
        """
        self.product = product
        self.html_string = ''  # html to return

    def get(self, key):
        """
        Simply return a product's data by key.
        :param key: Key's data to return.
        :return: self for further chaining
        """
        self.html_string = self.product[key]

        return self

    def refined(self):
        """
        Returns only the the text data form the specification we wish to work with.
        :return: self for further chaining
        """

        return self.from_spec_get(['general', 'Ports', 'Media_Formats'])

    def from_spec_get(self, ul_ids):
        """
        Extract specific keys from a product's spec. based on the html <ul> tag ids.

        :param ul_ids: List of ids to extract
        :return: self for further chaining
        """
        soup = bs(self.html_string, 'html.parser')

        self.html_string = ''
        for ul_id in ul_ids:
            self.html_string += soup.find(id=ul_id).prettify()

        return self

    def html(self):
        """
        Return the raw html
        :return: HTML
        """
        return self.html_string

    def text(self):
        """
        Returns the parsed HTML as plain text
        :return: plain text
        """
        return self.parsed_html()

    def prettify(self):
        """
        Prettify returns formatted HTML instead of a single string.
        i.e <ul><li>OS: Android 5.1</li><ul> becomes
        <ul>
          <li>OS: Android 5.1</li>
        <ul>
        :return: formatted HTML
        """
        try:
            soup = bs(self.html_string, 'html.parser')

        # If TypeError is thrown just return the raw html
        # this usually happens when a int is passed such
        # as the products id.
        except TypeError:
            return self.html_string

        return soup.prettify()

    def parsed_html(self):
        """
        Parses the html and returns a formatted plain text string.
        :return: string
        """
        try:
            # Strip HTML tags and whitespace.
            soup = bs(self.html_string, 'html.parser')

            output = ''
            for string in soup.stripped_strings:
                output += string + '\n'

        # If TypeError is thrown just return the raw html
        # this usually happens when a int is passed such
        # as the products id.
        except TypeError:
            return self.html_string

        return output
