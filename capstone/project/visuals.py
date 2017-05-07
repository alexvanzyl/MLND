import numpy as np
import pandas as pd
from product import Product
import matplotlib.pyplot as plt
from engine import matching_score
from product_transform import Transform


def plot_word_count_graph(refine_spec=False):
    """
    Plot area chart of all product specification word counts and the average.
    """

    word_counts = np.array(get_product_spec_word_counts(refine=refine_spec))

    rms = np.sqrt(np.mean(np.square(word_counts)))
    print('RMS word count is %d' % rms)
    print('Average word count is %d' % word_counts.mean())
    print('Maximum word count is %d' % word_counts.max())
    print('Minimum word count is %d' % word_counts.min())

    data = {'Word count': word_counts, 'RMS': rms}

    df = pd.DataFrame(data=data)
    ax = df.plot.area(stacked=False, title="Word count for each product spec.", figsize=(15, 10), legend=True,
                      fontsize=12)
    ax.set_ylabel("Word count", fontsize=12)
    plt.show()


def plot_product_scores(product_id, scores):
    """
    Plot bar chat of similarity and matching scores.

    :param product_id:
    :param scores
    :return:
    """

    similarity_scores = []
    related_item_ids = []
    matching_scores = []
    for score in scores:
        similarity_score, item_id = score
        related_item_ids.append(item_id)
        similarity_scores.append(similarity_score)
        matching_scores.append(matching_score(parent_id=product_id, item_id=item_id))

    data = {'Matching score': matching_scores, 'Similarity score': similarity_scores, 'Product id': related_item_ids}

    df = pd.DataFrame(data=data)
    ax = df.plot.bar(x='Product id', stacked=False, title="Matching and similarity scores", figsize=(8, 6), legend=True,
                     fontsize=12)
    ax.set_ylabel("Scores", fontsize=12)
    plt.show()

    print('Similarity scores: {}'.format(similarity_scores))
    print('Matching scores: {}'.format(matching_scores))
    print('Mean difference: {}'.format(mean_diff(similarity_scores, matching_scores)))


def get_product_spec_word_counts(refine=False):
    # Grab all the products and count the words in each specification

    word_counts = []
    for product in Product().get_all():
        if refine:
            word_counts.append(len(Transform(product).get('specification').refined().text().split()))
        else:
            word_counts.append(len(Transform(product).get('specification').text().split()))

    return word_counts


def mean_diff(similarity_scores, matching_scores):
    # calculate the average difference between similarity and matching scores.
    return abs(np.mean(np.array(similarity_scores) - np.array(matching_scores)))