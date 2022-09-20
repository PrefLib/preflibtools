""" This module presents procedures to convert instances from one type to another.
"""
from preflibtools.properties.basic import pairwise_scores


def order_to_pwg(instance):
    """ Takes as input an instances and returns a string describing a pairwise graph.

        :param instance: The instance to convert.
        :type instance: :class:`preflibtools.instances.preflibinstance.OrdinalInstance`
    """
    header = str(instance.num_alternatives) + "\n"
    for alt, alt_name in instance.alternatives_name.items():
        header += str(alt) + "," + str(alt_name) + "\n"
    header = header

    scores = pairwise_scores(instance)
    pairwise_relation = ""
    sum_vote_count = 0
    num_unique = 0
    for alt_name1, score_dict in scores.items():
        for alt_name2, score in score_dict.items():
            pairwise_relation += str(score) + "," + str(alt_name1) + "," + str(alt_name2) + "\n"
            num_unique += 1
            sum_vote_count += score
    pairwise_relation = pairwise_relation[:-1]

    count_line = str(instance.num_voters) + "," + str(sum_vote_count) + "," + str(num_unique) + "\n"

    return header + count_line + pairwise_relation
