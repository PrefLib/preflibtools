""" This module provides procedures to check if an instance describes preferences that are single-crossing.
"""


def is_single_crossing(instance):
    """Tests whether the instance describe a profile of single-crossed preferences.

    :param instance: The instance to take the orders from.
    :type instance: preflibtools.instances.preflibinstance.OrdinalInstance

    :return: A boolean indicating whether the instance is single-crossed or no.
    :rtype: bool
    """

    def prefers(a, b, o):
        return o.index(a) < o.index(b)

    def conflict_set(o1, o2):
        res = set([])
        for i in range(len(o1)):
            for j in range(i + 1, len(o1)):
                if (prefers(o1[i], o1[j], o1) and prefers(o1[j], o1[i], o2)) or (
                    prefers(o1[j], o1[i], o1) and prefers(o1[i], o1[j], o2)
                ):
                    res.add((min(o1[i][0], o1[j][0]), max(o1[i][0], o1[j][0])))
        return res

    def is_SC_with_first(i, profile):
        for j in range(len(profile)):
            for k in range(len(profile)):
                conflict_ij = conflict_set(profile[i], profile[j])
                conflict_ik = conflict_set(profile[i], profile[k])
                if not (
                    conflict_ij.issubset(conflict_ik)
                    or conflict_ik.issubset(conflict_ij)
                ):
                    return False
        return True

    for i in range(len(instance.orders)):
        if is_SC_with_first(i, instance.orders):
            return True
    return False
