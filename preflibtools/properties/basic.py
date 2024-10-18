""" This module describes several procedures to check for basic procedures of PrefLib instances.
"""
from preflibtools.instances import OrdinalInstance, CategoricalInstance
from preflibtools.properties.decorators import requires_preference_type


def num_alternatives(instance):
    """Returns the number of alternatives of the instance.

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: The number of alternatives of the instance.
    :rtype: int
    """
    return instance.num_alternatives


def num_voters(instance):
    """Returns the number of voters .

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: The number of voters of the instance.
    :rtype: int
    """
    return instance.num_voters


@requires_preference_type("toc", "soc", "toi", "soi", "cat")
def num_different_preferences(instance):
    """Returns the number of different orders of the instance.

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: The number of different orders of the instance.
    :rtype: int
    """
    if instance.data_type in ("toc", "soc", "toi", "soi"):
        return instance.num_unique_orders
    elif instance.data_type == "cat":
        return instance.num_unique_preferences


@requires_preference_type("toc", "soc", "toi", "soi", "cat")
def largest_ballot(instance):
    """Returns the size of the largest ballot of the instance, i.e., the maximum number of alternatives
    appearing in an order.

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: The size of the largest ballot of the instance.
    :rtype: int
    """
    return max(
        [sum([len(pref_class) for pref_class in pref]) for pref in instance.preferences]
    )


@requires_preference_type("toc", "soc", "toi", "soi", "cat")
def smallest_ballot(instance):
    """Returns the size of the smallest ballot of the instance, i.e., the smallest number of alternatives
    appearing in an order.

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: The size of the smallest ballot of the instance.
    :rtype: int
    """
    return min(
        [sum([len(pref_class) for pref_class in pref]) for pref in instance.preferences]
    )


@requires_preference_type("toc", "soc", "toi", "soi", "cat")
def max_num_indif(instance):
    """Returns the maximum number of indifference classes over the orders of the instance.

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: The maximum number of indifference classes of the instance.
    :rtype: int
    """
    return max([len([p for p in o if len(p) > 1]) for o in instance.preferences] + [0])


@requires_preference_type("toc", "soc", "toi", "soi", "cat")
def min_num_indif(instance):
    """Returns the minimum number of indifference classes over the orders of the instance.

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: The minimum number of indifference classes of the instance.
    :rtype: int
    """
    return min(
        [len([p for p in o if len(p) > 1]) for o in instance.preferences]
        + [instance.num_alternatives]
    )


@requires_preference_type("toc", "soc", "toi", "soi", "cat")
def largest_indif(instance):
    """Returns the size of the largest indifference class of any voter of the instance.

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: The size of the largest indifference class of the instance.
    :rtype: int
    """
    return max([len(p) for o in instance.preferences for p in o if len(p) > 0] + [0])


@requires_preference_type("toc", "soc", "toi", "soi", "cat")
def smallest_indif(instance):
    """Returns the size of the smallest indifference class of any voter of the instance.

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: The size of the smallest indifference class of the instance.
    :rtype: int
    """
    return min(
        [len(p) for o in instance.preferences for p in o if len(p) > 0]
        + [instance.num_alternatives]
    )


@requires_preference_type("toc", "soc", "toi", "soi", "cat")
def is_approval(instance):
    """Checks whether the instance describes an approval profile. A profile is considered to represent approval
    ballots in two cases: All the orders are complete and consist of only two indifference classes; The orders
    are incomplete and consists of a single indifference class.

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: A boolean indicating whether the instance describes an approval profile.
    :rtype: bool
    """
    if isinstance(instance, OrdinalInstance):
        m = max([len(order) for order in instance.orders])
        return m == 1 or (m == 2 and is_complete(instance))
    elif isinstance(instance, CategoricalInstance):
        return instance.num_categories == 1 or (instance.num_categories == 2 and is_complete(instance))


@requires_preference_type("toc", "soc", "toi", "soi")
def is_strict(instance):
    """Checks whether the instance describes a profile of strict preferences.

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: A boolean indicating whether the instance describes a profile of strict preferences.
    :rtype: bool
    """
    return largest_indif(instance) == 1


@requires_preference_type("toc", "soc", "toi", "soi", "cat")
def is_complete(instance):
    """Checks whether the instance describes a profile of complete preferences.

    :param instance: The instance.
    :type instance: preflibtools.instances.preflibinstance.PreflibInstance

    :return: A boolean indicating whether the instance describes a profile of complete preferences.
    :rtype: bool
    """
    return smallest_ballot(instance) == instance.num_alternatives
