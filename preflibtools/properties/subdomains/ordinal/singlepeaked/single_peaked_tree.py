from __future__ import annotations

from collections.abc import Collection

from preflibtools.instances import OrdinalInstance

def get_bottom_alts(instance: list):
    """Get the set of last ranked alternatives in the instance.

    Args:
        instance (OrdinalInstance): the instance

    Returns:
        set: the set of last ranked alternatives
    """
    last_ranked = set()

    for voter in instance:
        last_ranked.add(voter[-1])

    return last_ranked


def restrict_preferences(profile: list[tuple], alternatives_set: Collection):
    """Restrict the preferences of the voters to elements in alternatives_set.

    Returns:
        (list): the restricted preferences
    """
    preferences = []
    for order in profile:
        pref = [c for c in order if c in alternatives_set]
        preferences.append(pref)
    return preferences

def get_B(profile: list[tuple], alt_set: Collection, alternative: int):
    # B_vals = []
    B_a = set()

    # TODO: Check if B_vals workaround works
    instance = restrict_preferences(profile, alt_set)

    for i in instance:
        # Check if top(i) = a
        # print("instance: ", i)
        # print("alternative: ", alternative)
        if alternative == i[0]:
            # B(i, a) = {second(i)}
            # B_vals.append(i[1])
            if len(i) != 1:
                B_a.add(i[1])
        else:
            # get all alternatives before a
            # B_vals.append(i[:i.index(alternative)])
            if len(B_a) == 0:
                B_a = set(i[:i.index(alternative)])
            else:
                B_a = B_a.intersection(set(i[:i.index(alternative)]))

    return B_a

def is_single_peaked_on_tree(instance: OrdinalInstance):
    """Function to detect whether or not the instance is single-peaked on a
    tree. Returns True and the tree on the set of alternatives such that the
    instance is single-peaked on this tree, if one exists. Based on Trick's
    1989 algorithm.

    Args:
        instance (OrdinalInstance): the preference data
    """
    C_set = set(instance.alternatives_name)

    orders = [o for o, m in instance.flatten_strict()]

    # print("C_set: ", C_set)
    tree = []

    while len(C_set) >= 3:
        L_set = get_bottom_alts(restrict_preferences(orders, C_set))
        # print("L_set: ", L_set)

        for a in L_set:
            # print("C_set in for: ", C_set)
            B_a = get_B(orders, C_set, a)
            # print(f"a: {a}, B_a: {B_a}")
            if B_a:
                b = B_a.__iter__().__next__()

                tree.append((b, a))
                C_set.remove(a)
                # print("C_set removed: ", C_set)

            else:
                # instance is not single-peaked on any tree
                return False, None

    if len(C_set) == 2:
        # add edge (a, b) to T
        # print("C_set new: ", C_set)

        a, b = C_set
        # print(f"edge: {a, b}")
        tree.append((a, b))

    return True, tree

