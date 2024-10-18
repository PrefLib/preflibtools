""" This module describes several procedures to check for properties based on pairwise comparisons.
"""

from preflibtools.properties import requires_preference_type

from collections import defaultdict


@requires_preference_type("soc", "toc", "soi", "toi")
def pairwise_scores(instance):
    """Returns a dictionary of dictionaries mapping every alternative a to the number of times it beats
    every other alternative b (the number of voters preferring a over b).

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: A dictionary of dictionaries storing the scores.
    :rtype: dict
    """
    scores = {
        alt: {a: 0 for a in instance.alternatives_name if a != alt}
        for alt in instance.alternatives_name
    }
    for order in instance.orders:
        alternatives_before = []
        for indif_class in order:
            # Every alternative appearing before are beating the ones in the current indifference class
            for alt_beaten in indif_class:
                for alt_winning in alternatives_before:
                    scores[alt_winning][alt_beaten] += instance.multiplicity[order]
            alternatives_before += [alt for alt in indif_class]
    return scores


@requires_preference_type("soc", "toc", "soi", "toi")
def copeland_scores(instance):
    """Returns a dictionary of dictionaries mapping every alternative a to their Copeland score against every other
    alternative b (the number of voters preferring a over b minus the number of voters preferring b over a).

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: A dictionary of dictionaries storing the scores.
    :rtype: dict
    """
    scores = {
        alt: {a: 0 for a in instance.alternatives_name if a != alt}
        for alt in instance.alternatives_name
    }
    for order in instance.orders:
        alternatives_before = []
        for indif_class in order:
            # Every alternative appearing before are beating the ones in the current indifference class
            for alt_beaten in indif_class:
                for alt_winning in alternatives_before:
                    scores[alt_winning][alt_beaten] += instance.multiplicity[order]
                    scores[alt_beaten][alt_winning] -= instance.multiplicity[order]
            alternatives_before += [alt for alt in indif_class]
    return scores


@requires_preference_type("soc", "toc", "soi", "toi")
def has_condorcet(instance, weak_condorcet=False):
    """Checks whether the instance has a Condorcet winner, using different procedures depending on the data type of
    the instance. An alternative is a Condorcet winner if it strictly beats every other alternative in a pairwise
    majority contest. An alternative is a weak Condorcet winner if it strictly beats or ties every other
    alternative in a pairwise majority contest.

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance
    :param weak_condorcet: Boolean indicating whether to consider weak-Condorcet winners or not.
    :type weak_condorcet: bool

    :return: A boolean indicating whether the instance has a Condorcet winner or not.
    :rtype: bool
    """
    scores = copeland_scores(instance)
    for alt, scoreDict in scores.items():
        if all(
            score > 0 or (weak_condorcet and score >= 0) for score in scoreDict.values()
        ):
            return True
    return False


@requires_preference_type("toc", "soc")
def borda_scores(instance):
    """Computes the total Borda scores of all the alternatives of the instance. Within an indifference class, all
    alternatives are assigned the smallest score one alternative from the class would have gotten, had the order
    been strict. For instance, for the order ({a1}, {a2, a3}, {a4}), a1 gets score 3, a2 and a3 score 1 and a4
    score 0.

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: A dictionary mapping every instance to their Borda score.
    :rtype: dict
    """
    res = defaultdict(lambda: 0)
    for order in instance.orders:
        multiplicity = instance.multiplicity[order]
        i = instance.num_alternatives
        for indif_class in order:
            i -= len(indif_class)
            for alt in indif_class:
                res[alt] += i * multiplicity
    return res
