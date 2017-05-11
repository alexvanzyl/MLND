import numpy as np
import pandas as pd
from product import Product
import matplotlib.pyplot as plt
from product_transform import Transform


def show_top_weighted_terms(tfidf_matrix, vector, n_top=10):
    print('sparse matrix shape:', tfidf_matrix.shape)
    print('nonzero count: {} out of {}:'.format(tfidf_matrix.nnz, np.prod(tfidf_matrix.shape)))
    print('sparsity: %.2f%%' % sparsity(tfidf_matrix))

    weights = np.asarray(tfidf_matrix.sum(axis=0)).ravel().tolist()
    weights_df = pd.DataFrame({'term': vector.get_feature_names(), 'weight': weights})

    return weights_df.sort_values(by='weight', ascending=False).head(n_top)


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


def plot_product_scores(product_id, engine, show_values=False):
    """
    Plot bar chat of similarity scores.

    :param product_id:
    :param engine
    :param show_values:
    :return:
    """

    model_selected_item_scores, manually_selected_item_scores, related_item_ids = parse_scores(product_id, engine)

    data = {
        'Model selected': model_selected_item_scores,
        'Manually selected': manually_selected_item_scores,
        'Product id': [related_item_ids[:2], related_item_ids[2:4], related_item_ids[4:6]]
    }

    df = pd.DataFrame(data=data)
    ax = df.plot.bar(x='Product id', stacked=False,
                     title="Top 3 Manual vs. Model Selected - Similarity scores for product ID %d" % product_id,
                     figsize=(8, 6), legend=True, fontsize=12, rot=0)

    # Move legend outside of the graph
    ax.legend(bbox_to_anchor=(1, 1), loc=2)

    # show value on top of each bar.
    if show_values:
        for idx, rect in enumerate(ax.patches):
            # Set height of every second label higher for readability
            height = rect.get_height()
            if idx % 2:
                height = rect.get_height() * 1.0

            # rect.get_x() + rect.get_width() / 2.
            ax.text(rect.get_x() + rect.get_width() / 2, height,
                    '%.3f' % float(rect.get_height()), ha='center',
                    va='bottom')

        # update the y-axis size so text stays within the frame.
        ax.axis(ymax=max(model_selected_item_scores) + 0.05)

    ax.set_ylabel("Similarity score", fontsize=12)
    plt.show()


def parse_scores(product_id, engine):
    # Splits the related item's id an score from a tuple
    # and creates two lists one with all the scores
    # and the other with all the related item ids.
    scores = engine.get_product_similarity_scores(product_id)

    model_selected_item_scores = []
    manually_selected_item_scores = []
    related_item_ids = []

    manually_selected_items = Product().get_manually_selected_related_items(product_id)

    # We only want the top 3 scores
    for idx, score in enumerate(scores[:3]):
        sim_score, item_id = engine.get_similar_score_for_item(
            manually_selected_items[idx]['product_id'], scores, as_tuple=True)
        manually_selected_item_scores.append(sim_score)
        related_item_ids.append(item_id)

        sim_score, item_id = score
        model_selected_item_scores.append(sim_score)
        related_item_ids.append(item_id)

    return model_selected_item_scores, manually_selected_item_scores, related_item_ids


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


def sparsity(tfidf_matrix):
    # calculate the sparsity,
    return 100.0 * (1 - tfidf_matrix.nnz / np.prod(tfidf_matrix.shape))
