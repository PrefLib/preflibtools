"""
Euclidean domain for ordinal preferences.
"""
from __future__ import annotations

from preflibtools.instances import OrdinalInstance
from preflibtools.properties.subdomains.ordinal.singlecrossing import is_single_crossing

import itertools

from mip import Model, CONTINUOUS, minimize, xsum, OptimizationStatus


def _append_to_axis(axis: list, a: int, b:int):
    """Adds alternatives a and b to the axis in such a way that a is to the
    left of b.

    Args:
        axis (list): the axis to append to
        a (int): first alternative
        b (int): second alternative

    Returns:
        (list): the updated axis
    """
    if a not in axis:
        axis.append(a)

    idx_a = axis.index(a)

    if b in axis:
        idx_b = axis.index(b)
        if idx_b < idx_a:
            axis.remove(b)
            axis.append(b)
    else:
        axis.append(b)

    # print("\taxis after:", axis)
    return axis


def _restrict_preferences(instance: OrdinalInstance, C_set_plus: set):
    """Restrict the preferences of the voters to elements in C_set_plus.

    Returns:
        (list): the restricted preferences
    """
    flattened = instance.flatten_strict()

    preferences = []
    for (pref, _) in flattened:
        pref = [c for c in pref if c in C_set_plus]
        preferences.append(pref)

    return preferences


def _one_euclidean_solve_lp(preferences: list, axis: list):
    """Attempts to solve the linear program for the 1-Euclidean domain,
    given the preferences and the axis. Makes use of the MIP library.

    Args:
        preferences (list): the preferences of the voters
        axis (list): the axis for which the profile is single-crossing

    Returns:
        (model.status, list, dict): tuple containing the status of the LP, the
        voters and the alternatives if the LP is feasible, None otherwise.
    """
    # create pairs (a, b) such that a is to the left of b in the axis
    pairs = [(a, b) for a, b in itertools.combinations(axis, 2)
             if axis.index(a) < axis.index(b)]

    n = len(preferences)
    m = len(axis)

    model = Model()

    # add variables for the voters and alternatives
    all_vars = [model.add_var(var_type=CONTINUOUS, name=f"voter_{i}") for i in range(n)]
    all_vars += [model.add_var(var_type=CONTINUOUS, name=f"alternative_{axis[i]}") for i in range(m)]

    #TODO: var for axis.index(pair[0]) etc.

    for pair in pairs:
        # add axis constraints
        # print("pair:", pair)
        # model += vars[n + pair[0] - 1] + 1 <= vars[n + pair[1] - 1]
        # print("n + axis.index(pair[0]) - 1: ", n + axis.index(pair[0]) - 1)
        # print("n + axis.index(pair[1]) - 1: ", n + axis.index(pair[1]) - 1)
        # print("vars[n + axis.index(pair[1]) - 1]: ", vars[n + axis.index(pair[1]) - 1])
        model += all_vars[n + axis.index(pair[0])] + 1 <= all_vars[n + axis.index(pair[1])]
        # add voter constraints
        for i in range(n):
            # if voter prefers a to b
            if preferences[i].index(pair[0]) < preferences[i].index(pair[1]):
                # model += vars[i] + 1 <= (vars[n + pair[0] - 1] + vars[n + pair[1] - 1]) / 2
                model += all_vars[i] + 1 <= (all_vars[n + axis.index(pair[0])] + all_vars[n + axis.index(pair[1])]) / 2
            else:
                # model += vars[i] >= (vars[n + pair[1] - 1] + vars[n + pair[0] - 1]) / 2 + 1
                model += all_vars[i] >= (all_vars[n + axis.index(pair[1])] + all_vars[n + axis.index(pair[0])]) / 2 + 1


    model.objective = minimize(xsum(all_vars))

    # suppress log
    model.verbose = 0

    status = model.optimize()

    if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
        alternatives = dict()
        for i in range(m):
            alternatives[axis[i]] = all_vars[n + i].x

        voters = []
        for i in range(n):
            voters.append(all_vars[i].x)

        return status, voters, alternatives

    return None, None, None


def _one_euclidean_gen_sets(v_1: list, C_set_plus: set, C_set_minus: set):
    """Generates the sets F and G for the 1-Euclidean domain.

    Args:
        v_1 (list): the preferences of the first voter
        C_set_plus (set): the set of alternatives in C_set_plus
        C_set_minus (set): the set of alternatives in C_set_minus

    Returns:
        (list, list, int): tuple containing the sets F and G, and the number of
        sets in F (k).
    """
    f, g = dict(), dict()
    ind = 0

    # if C_set_minus is empty
    if not C_set_minus:
        return [C_set_plus], [], 1

    while C_set_minus and C_set_plus:
        tmp = None
        while C_set_plus:
            a = C_set_plus.pop()

            for b in C_set_minus:
                if v_1.index(a) > v_1.index(b):
                    if tmp is None:
                        ind += 1
                    tmp = b

                    if not ind in f:
                        f[ind] = set()
                    f[ind].add(a)
                else:
                    if not ind in f:
                        f[ind] = set()
                    f[ind].add(a)


        if tmp is not None:
            C_set_minus.remove(tmp)
            if not ind in g:
                g[ind] = set()
            g[ind].add(tmp)

        ind += 1
        g[ind] = C_set_minus

    return list(f.values()), list(g.values()), len(f)


def is_one_euclidean(instance: OrdinalInstance):
    """Check if the given instance is in the 1-Euclidean domain.

    Args:
        instance (OrdinalInstance): the preference profile

    Returns:
        (Boolean, dict): True and the mapping of voters to alternatives if the
        instance is in the 1-Euclidean domain, False and None otherwise.
    """

    is_SC, _ = is_single_crossing(instance)
    # verify that E is single-crossing
    if is_SC:
        # get the first voter
        v_1 = list(instance.flatten_strict()[0][0])
        # get the top of the first voter
        c_minus = v_1[0]

        # get the last voter
        v_n = list(instance.flatten_strict()[-1][0])
        # get the top of the last voter
        c_plus = v_n[0]

        C_set = set(instance.alternatives_name)
        m = len(C_set)

        # number of voters
        n = len(instance.orders)
        gamma = dict()

        # walk through the alternatives
        # colour the alternatives:
        #   - red: if c in C_M (0)
        #   - blue: if c in C_R (1)
        #   - green: if c in C_L (2)
        #   - grey: else (3)
        for c in C_set:
            if ((v_1.index(c) < v_1.index(c_plus)
                and v_n.index(c) < v_n.index(c_minus))
                or (c in {c_minus, c_plus})):
                # put c in C_M
                gamma[c] = 0
            else:
                # put in else
                gamma[c] = 3

        # walk through the alternatives in pairs
        # TODO: check if the order of the pairs is important
        for a, b in itertools.permutations(C_set, 2):
            if (v_1.index(a) < v_1.index(b)
                and v_n.index(b) < v_n.index(a)):
                if gamma[a] == 1 or gamma[b] == 2:
                    # Colouring stage cannot be completed
                    return False, None
                if gamma[a] == 3:
                    gamma[a] = 2
                if gamma[b] == 3:
                    gamma[b] = 1

        C_set_plus = set([c for c in C_set if gamma[c] != 3])
        C_set_minus = C_set - C_set_plus

        # create axis_dict with alternatives as keys and values as lists
        axis_dict = dict()
        for c in C_set_plus:
            axis_dict[c] = 0

        # walk through the alternatives in C_set_plus in pairs
        for a, b in itertools.combinations(C_set_plus, 2):
            # print(a, b)
            if ((gamma[a] == 2 and gamma[b] == 0)
                or (gamma[a] == 0 and gamma[b] == 1)
                or (gamma[a] == 2 and gamma[b] == 1)):
                # axis = _append_to_axis(axis, a, b)
                axis_dict[a] += 1

            elif ((gamma[b] == 2 and gamma[a] == 0)
                or (gamma[b] == 0 and gamma[a] == 1)
                or (gamma[b] == 2 and gamma[a] == 1)):
                # axis = _append_to_axis(axis, b, a)
                axis_dict[b] += 1

            elif ((gamma[a] == 0 and gamma[b] == 0)
                or (gamma[a] == 1 and gamma[b] == 1)):

                a_indx = v_1.index(a)
                b_indx = v_1.index(b)

                if a_indx < b_indx:
                    # axis = _append_to_axis(axis, a, b)
                    axis_dict[a] += 1
                else:
                    # axis = _append_to_axis(axis, b, a)
                    axis_dict[b] += 1

            elif gamma[a] == 2 and gamma[b] == 2:

                a_n_indx = v_n.index(a)
                b_n_indx = v_n.index(b)

                if a_n_indx < b_n_indx:
                    # axis = _append_to_axis(axis, b, a)
                    axis_dict[b] += 1
                else:
                    # axis = _append_to_axis(axis, a, b)
                    axis_dict[a] += 1

        # base axis on value of axis_dict
        axis = [k for k, v in sorted(axis_dict.items(), key=lambda item: item[1], reverse=True)]

        # restrict the preferences of the voters to elements in C_set_plus
        preferences = _restrict_preferences(instance, C_set_plus)

        # TODO: return voters as dict for mapping?
        # TODO: rename alternatives to x for consistency
        results, voters, alternatives = _one_euclidean_solve_lp(preferences, axis)

        # check if the LP is feasible
        if results is not None:
            # insert grey alternatives in the axis
            # partition the grey and non-grey alternatives into groups
            # according to the order of their appearance in the preference of
            # the first voter.
            f, g, k = _one_euclidean_gen_sets(v_1, C_set_plus, C_set_minus)

            # TODO: check if tmp construction is ever needed since mapping will only be constructed for non-grey value

            # union V and F1
            tmp = voters + [alternatives[i] for i in f[0]]


            # TODO: check if index or value is needed
            x_l = min(tmp)
            x_r = max(tmp)

            tmp = voters + [alternatives[i] for i in C_set_plus]

            # TODO: see previous comment, delta currently as value
            delta = max([abs(x - y) for x, y in itertools.permutations(tmp, 2)])

            y = dict()
            # add mapping of voters
            # index: 1 to n
            for i in range(n):
                y[i] = voters[i]

            # add F1 mapping
            for i in range(len(f[0])):
                # pop add method for efficiency
                tmp = f[0].pop()
                f[0].add(tmp)
                y[tmp + n - 1] = alternatives[tmp]

            # add mapping of grey alternatives in G1
            if g:
                for i in range(len(g[0])):
                    tmp = g[0].pop()
                    g[0].add(tmp)
                    y[tmp + n - 1] = x_r + 6 * delta + (i / m) * delta


            for i in range(1, k):
                for c in f[i]:
                    if alternatives[c] < x_l:
                        y[c + n - 1] = alternatives[c] - ((i + 1)**2) * delta
                    if alternatives[c] > x_r:
                        y[c + n - 1] = alternatives[c] + ((i + 1)**2) * delta

                for l in range(len(g[i])):
                    y[g[i].pop() + n - 1] = x_r + ((i + 1)**2) * delta + 2 * delta + l / m * delta

            return True, y

    return False, None
