import time
import pandas as pd
from product import Product
from product_transform import Transform
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


class Engine:
    def __init__(self):
        self.similarities = []
        self.tfidf_matrix = []

    def train_on(self, key, **kwargs):
        """
        Fit the TfidfVectorizer and calculate the cosine similarity

        :param key: The selected text to train our tf-idf vector i.e 'specification', 'refined_specification.
        :param kwargs: Further custom parameters we can pass to TfidfVectorizer
        :return: TfidfVectorizer
        """

        text_data = self.get_text_data(key)
        start = time.time()

        tf = TfidfVectorizer(analyzer='word', stop_words='english', **kwargs)
        self.tfidf_matrix = tf.fit_transform(text_data['text'])

        print("Engine trained in %s seconds." % (time.time() - start))

        self.set_similarities(text_data)

        return tf

    def set_similarities(self, text_data):
        """
        Return a list of all similar items for each product based
        on what was calculated by cosine similarity equation.
        :param text_data: DataFrame of the text used to train tf-idf.
        :return: custom list of similarity scores.
        """

        cosine_similarities = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

        self.similarities = []
        for idx, row in text_data.iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-66:-1]
            similar_items = [(cosine_similarities[idx][i], text_data['product_id'][i]) for i in similar_indices]
            self.similarities.append({similar_items[0][1]: similar_items[1:]})

        return self.similarities

    def get_product_similarity_scores(self, product_id):
        """
        Get all related items for a specific product.

        :param product_id:
        :return: product
        """
        for product in self.similarities:
            if product_id in product.keys():
                return product[product_id]

    def get_similar_score_for_item(self, product_id, scores, as_tuple=False):
        """
        Get the similarity score for a single item related to a product.

        :param product_id:
        :param scores:
        :return: similarity score
        """
        for idx, score in enumerate(scores):
            if score[1] == product_id:
                if as_tuple:
                    return score
                else:
                    return score[0]



    def get_text_data(self, key):
        """
        Returns the parsed text data to be used by tf-idf.

        :param key:
        :return: Dataframe
        """
        start = time.time()
        data = []
        for product in Product().get_all():
            if key == 'refined_specification':
                text = Transform(product).get('specification').refined().text().lower()
            else:
                text = Transform(product).get(key).text().lower()

            data.append({'product_id': product['id'], 'text': text})

        print("Text parsed in %s seconds." % (time.time() - start))

        return pd.DataFrame(data)


def get_refined_spec_word_list(product_id):
    """
    Takes a products spec. and splits it into a list of words.

    :param product_id:
    :return: list of words.
    """
    return Transform(Product().find_by_id(product_id)) \
        .get('specification') \
        .refined() \
        .text() \
        .lower() \
        .split()
