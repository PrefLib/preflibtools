""" This module describes several procedures to check for basic procedures of PrefLib instances.
"""


def pairwise_scores(instance):
    """ Returns a dictionary of dictionaries mapping every alternative a to the number of times it beats
        every other alternative b (the number of voters preferring a over b).

        :param instance: The instance.
        :type instance: preflibtools.instance.preflibinstance.PreflibInstance

        :return: A dictionary of dictionaries storing the scores.
        :rtype: dict
    """
    if instance.data_type in ["soc", "toc", "soi", "toi"]:
        scores = {alt: {a: 0 for a in instance.alternatives_name if a != alt} for alt in instance.alternatives_name}
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
    """ Returns a dictionary of dictionaries mapping every alternative a to their Copeland score against every other
        alternative b (the number of voters preferring a over b minus the number of voters preferring b over a).

        :param instance: The instance.
        :type instance: preflibtools.instance.preflibinstance.PreflibInstance

        :return: A dictionary of dictionaries storing the scores.
        :rtype: dict
    """
    if instance.data_type in ["soc", "toc", "soi", "toi"]:
        scores = {alt: {a: 0 for a in instance.alternatives_name if a != alt} for alt in instance.alternatives_name}
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
    """ Checks whether the instance has a Condorcet winner, using different procedures depending on the data type of
        the instance. An alternative is a Condorcet winner if it strictly beats every other alternative in a pairwise
        majority contest. 

        :param instance: The instance.
        :type instance: preflibtools.instance.preflibinstance.PreflibInstance

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
    """ Computes the total Borda scores of all the alternatives of the instance. Within an indifference class, all
        alternatives are assigned the smallest score one alternative from the class would have gotten, had the order
        been strict. For instance, for the order ({a1}, {a2, a3}, {a4}), a1 gets score 3, a2 and a3 score 1 and a4 
        score 0.

        :param instance: The instance.
        :type instance: preflibtools.instance.preflibinstance.PreflibInstance

        :return: A dictionary mapping every instance to their Borda score.
        :rtype: dict
    """
    if instance.data_type not in ("toc", "soc"):
        raise TypeError("You are trying to compute the Borda scores of an instance of type " +
                        str(instance.data_type) + ", this is not possible.")
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


def num_alternatives(instance):
    """ Returns the number of alternatives of the instance.

        :param instance: The instance.
        :type instance: preflibtools.instance.preflibinstance.PreflibInstance

        :return: The number of alternatives of the instance.
        :rtype: int
    """
    return instance.num_alternatives


def num_voters(instance):
    """ Returns the number of voters .

        :param instance: The instance.
        :type instance: preflibtools.instance.preflibinstance.PreflibInstance

        :return: The number of voters of the instance.
        :rtype: int
    """
    return instance.num_voters


def num_different_preferences(instance):
    """ Returns the number of different orders of the instance.

        :param instance: The instance.
        :type instance: preflibtools.instance.preflibinstance.PreflibInstance

        :return: The number of different orders of the instance.
        :rtype: int
    """
    if instance.data_type in ("toc", "soc", "toi", "soi"):
        return instance.num_unique_orders
    elif instance.data_type == "cat":
        return instance.num_unique_preferences


def largest_ballot(instance):
    """ Returns the size of the largest ballot of the instance, i.e., the maximum number of alternatives 
        appearing in an order.

        :param instance: The instance.
        :type instance: preflibtools.instance.preflibinstance.OrdinalInstance

        :return: The size of the largest ballot of the instance.
        :rtype: int
    """
    return max([sum([len(indif_class) for indif_class in order]) for order in instance.orders])


def smallest_ballot(instance):
    """ Returns the size of the smallest ballot of the instance, i.e., the smallest number of alternatives 
        appearing in an order.

        :param instance: The instance.
        :type instance: preflibtools.instance.preflibinstance.OrdinalInstance

        :return: The size of the smallest ballot of the instance.
        :rtype: int
    """
    return min([sum([len(indif_class) for indif_class in order]) for order in instance.orders])


def max_num_indif(instance):
    """ Returns the maximum number of indifference classes over the orders of the instance.

        :param instance: The instance.
        :type instance: preflibtools.instance.preflibinstance.OrdinalInstance

        :return: The maximum number of indifference classes of the instance.
        :rtype: int
    """
    return max([len([p for p in o if len(p) > 1]) for o in instance.orders] + [0])


def min_num_indif(instance):
    """ Returns the minimum number of indifference classes over the orders of the instance.

        :param instance: The instance.
        :type instance: preflibtools.instance.preflibinstance.OrdinalInstance

        :return: The minimum number of indifference classes of the instance.
        :rtype: int
    """
    return min([len([p for p in o if len(p) > 1]) for o in instance.orders] + [instance.num_alternatives])


def largest_indif(instance):
    """ Returns the size of the largest indifference class of any voter of the instance.

        :param instance: The instance.
        :type instance: preflibtools.instance.preflibinstance.OrdinalInstance

        :return: The size of the largest indifference class of the instance.
        :rtype: int
    """
    return max([len(p) for o in instance.orders for p in o if len(p) > 0] + [0])


def smallest_indif(instance):
    """ Returns the size of the smallest indifference class of any voter of the instance.

        :param instance: The instance.
        :type instance: preflibtools.instance.preflibinstance.OrdinalInstance

        :return: The size of the smallest indifference class of the instance.
        :rtype: int
    """
    return min([len(p) for o in instance.orders for p in o if len(p) > 0] + [instance.num_alternatives])


def is_approval(instance):
    """ Checks whether the instance describes an approval profile. A profile is considered to represent approval 
        ballots in two cases: All the orders are complete and consist of only two indifference classes; The orders
        are incomplete and consists of a single indifference class.

        :param instance: The instance.
        :type instance: preflibtools.instance.preflibinstance.OrdinalInstance

        :return: A boolean indicating whether the instance describes an approval profile.
        :rtype: bool
    """
    m = max([len(order) for order in instance.orders])
    if m == 1:
        return True
    elif m == 2:
        return is_complete(instance)
    else:
        return False


def is_strict(instance):
    """ Checks whether the instance describes a profile of strict preferences.

        :param instance: The instance.
        :type instance: preflibtools.instance.preflibinstance.OrdinalInstance

        :return: A boolean indicating whether the instance describes a profile of strict preferences.
        :rtype: bool
    """
    return largest_indif(instance) == 1


def is_complete(instance):
    """ Checks whether the instance describes a profile of complete preferences.

        :param instance: The instance.
        :type instance: preflibtools.instance.preflibinstance.OrdinalInstance

        :return: A boolean indicating whether the instance describes a profile of complete preferences.
        :rtype: bool
    """
    return smallest_ballot(instance) == instance.num_alternatives
