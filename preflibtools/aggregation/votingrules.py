""" This module contains several voting methods to aggregate the preferences in an instance.
"""

def pairwise_scores(instance):
    """Returns a dictionary of dictionaries mapping every alternative a to the number of times it beats
    every other alternative b (the number of voters preferring a over b).

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: A dictionary of dictionaries storing the scores.
    :rtype: dict
    """
    if instance.data_type in ["soc", "toc", "soi", "toi"]:
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


def copeland_scores(instance):
    """Returns a dictionary of dictionaries mapping every alternative a to their Copeland score against every other
    alternative b (the number of voters preferring a over b minus the number of voters preferring b over a).

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: A dictionary of dictionaries storing the scores.
    :rtype: dict
    """
    if instance.data_type in ["soc", "toc", "soi", "toi"]:
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


def has_condorcet(instance):
    """Checks whether the instance has a Condorcet winner, using different procedures depending on the data type of
    the instance. An alternative is a Condorcet winner if it strictly beats every other alternative in a pairwise
    majority contest.

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: A boolean indicating whether the instance has a Condorcet winner or not.
    :rtype: bool
    """
    if instance.data_type in ["soc", "toc", "soi", "toi"]:
        scores = copeland_scores(instance)
        for alt, scoreDict in scores.items():
            if all(score > 0 for score in scoreDict.values()):
                return True
        return False


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
    if instance.data_type not in ("toc", "soc"):
        raise TypeError(
            "You are trying to compute the Borda scores of an instance of type "
            + str(instance.data_type)
            + ", this is not possible."
        )
    res = dict([])
    for order in instance.orders:
        multiplicity = instance.multiplicity[order]
        i = instance.num_alternatives
        for indif_class in order:
            i -= len(indif_class)
            for alt in indif_class:
                if alt not in res:
                    res[alt] = i * multiplicity
                else:
                    res[alt] += i * multiplicity
    return res
