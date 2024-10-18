""" This module presents procedures to convert instances from one type to another.
"""
from preflibtools.properties.pairwisecomparisons import pairwise_scores


def order_to_pwg(instance):
    """Takes as input an instances and returns a string describing a pairwise graph.

    :param instance: The instance to convert.
    :type instance: :class:`preflibtools.instances.preflibinstance.OrdinalInstance`
    """

    def concatenate_elements_with_delimiter(*args, delimiter=","):
        return delimiter.join(map(str, args)) + "\n"

    header = str(instance.num_alternatives) + "\n"
    for alt, alt_name in instance.alternatives_name.items():
        header += concatenate_elements_with_delimiter(alt, alt_name)

    scores = pairwise_scores(instance)
    pairwise_relation = ""
    sum_vote_count = 0
    num_unique = 0
    for alt_name1, score_dict in scores.items():
        for alt_name2, score in score_dict.items():
            pairwise_relation += concatenate_elements_with_delimiter(score, alt_name1, alt_name2)
            num_unique += 1
            sum_vote_count += score
    pairwise_relation = pairwise_relation[:-1]

    count_line = concatenate_elements_with_delimiter(instance.num_voters, sum_vote_count, num_unique)

    return header + count_line + pairwise_relation
