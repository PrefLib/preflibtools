""" This module provides procedures to deal with the potential single-peakedness of the instance.
"""

from __future__ import annotations

import copy
import time

from itertools import combinations

import numpy as np
from mip import Model, xsum, BINARY, MINIMIZE, INTEGER, OptimizationStatus

from preflibtools.properties.subdomains.consecutive_ones import isC1P


def is_single_peaked_axis(instance, axis):
    """Tests whether the instance is single-peaked with respect to the axis provided as argument.

    :param instance: the instance to work on.
    :type instance: preflibtools.instances.preflibinstance.OrdinalInstance
    :param axis: a list of candidates.
    :type axis: list

    :return: A boolean indicating if the instance is single-peaked with respect to axis.
    :rtype: bool
    """

    # Finds the position of the indifference class containing the alternative
    def indif_class_pos(order, alt):
        i = 0
        for indif_class in order:
            if alt in indif_class:
                return i
            i += 1

    if instance.data_type not in ("toc", "soc"):
        raise TypeError(
            "You are trying to test for single-peakedness on an instance of type "
            + str(instance.data_type)
            + ", this is not possible. Only toc and soc are allowed here."
        )

    for order in instance.orders:
        positions = [indif_class_pos(order, alt) for alt in axis]

        peak_passed = False
        previous_position = None
        for pos in positions:
            # If pos = 0, we are at the peak
            if pos == 0:
                peak_passed = True
            else:
                if previous_position is not None:
                    if peak_passed:
                        # If we passed the peak and the position is decreasing, there's a problem
                        if pos < previous_position:
                            return False
                    else:
                        # If we did not pass the peak and the position is increasing, there's a problem
                        if pos > previous_position:
                            return False
            previous_position = pos
    return True


def is_single_peaked(instance):
    """Tests whether the instance describes a profile of single-peaked preferences. It only works with strict
    preferences.

    This function implements the algorithm of Escoffier, Lang, and Ozturk (2008). We are grateful to Thor Yung
    Pheng who developed this function (under the supervision of Umberto Grandi).

    :param instance: the instance to test for single-peakedness.
    :type instance: preflibtools.instances.preflibinstance.OrdinalInstance

    :return: A Boolean indicating whether the instance is single-peaked, together with the axis with
        respect to which the instance would be single-peaked, the empty list if the instance is not
        single-peaked.
    :rtype: Tuple(bool, list)
    """

    if instance.data_type != "soc":
        raise TypeError(
            f"You are trying to use the algorithm of Escoffier, Lang, and Ozturk (2008) to test"
            f"single-peakedness on an instance of type {instance.data_type}, this is not possible."
        )

    is_SP = True
    end_flag = False
    axis = None
    right_axis, left_axis = [], []
    x_i, x_j = None, None
    to_append_left = [] # Candidates that will be appended to the left at the end

    # generates list of preferences without the weight while flattening the orders
    list_of_preferences = [
        list(orderMultiplicity[0]) for orderMultiplicity in instance.flatten_strict()
    ]

    # list_of_preferences_SP: list to modify
    list_of_preferences_SP = copy.deepcopy(list_of_preferences)

    while is_SP and len(list_of_preferences_SP[0]) >= 1 and not end_flag:
        # make a list of last candidates
        last_candidates = []
        for preference in list_of_preferences_SP:
            last_candidate = preference.pop()
            if last_candidate not in last_candidates:
                last_candidates.append(last_candidate)

        if (
            len(last_candidates) >= 3
        ):  # impossible to position all candidates in leftmost and rightmost axis
            is_SP = False
            end_flag = True

        elif len(last_candidates) == 1:
            x = last_candidates[0]
            for preference in list_of_preferences_SP:
                if x in preference:
                    preference.remove(x)

            if x_i is None:
                to_append_left.append(x)
            else:
                # Special case for the last candidate here i + 1 = j - 1
                if len(list_of_preferences_SP[0]) == 0:
                    left_axis.append(x)

                else:

                    case = 0

                    for i in range(len(list_of_preferences)):
                        # find index of x, x_i, x_j in each preference
                        index_x = list_of_preferences[i].index(x)
                        index_x_i = list_of_preferences[i].index(x_i)
                        index_x_j = list_of_preferences[i].index(x_j)

                        # 3 possibilities for len(last_candidates) == 1
                        if index_x_i > index_x > index_x_j:  # Case 3.(c) Inverse
                            if case == 2:
                                end_flag = True
                                is_SP = False  # contradiction
                                break
                            case = 1
                        elif index_x_j > index_x > index_x_i:  # Case 3.(c)
                            if case == 1:
                                end_flag = True
                                is_SP = False  # contradiction
                                break
                            case = 2
                        elif index_x < index_x_i and index_x < index_x_j:  # Case 3.(b)
                            pass
                        else:  # Case 3.(a) is impossible
                            raise ValueError("We should never have ended up here with a single "
                                             "candidate ranked last.")

                    # add x in leftmost or rightmost axis according to case if axis is compatible
                    if not end_flag:
                        if case == 0:
                            left_axis.append(x)
                            x_i = x
                        elif case == 1:
                            left_axis.append(x)
                            x_i = x
                        elif case == 2:
                            right_axis.insert(0, x)
                            x_j = x

        elif len(last_candidates) == 2:
            x, y = last_candidates
            for preference in list_of_preferences_SP:
                if x in preference:
                    preference.remove(x)
                if y in preference:
                    preference.remove(y)

            if x_i is None:
                left_axis.append(x)
                right_axis.insert(0, y)
                x_i = x
                x_j = y
            else:

                forced_position = {}
                for i in range(len(list_of_preferences)):
                    # find index of x, y, x_i, x_j in each preference
                    index_x = list_of_preferences[i].index(x)
                    index_y = list_of_preferences[i].index(y)
                    index_x_i = list_of_preferences[i].index(x_i)
                    index_x_j = list_of_preferences[i].index(x_j)

                    # swap position to put x in the lower position (ranked last)
                    if index_y > index_x:
                        index_x, index_y = index_y, index_x
                        x, y = y, x

                    # all possible cases
                    if index_x_j > index_x > index_y > index_x_i:  # Case 2.(d) Reverse
                        placed_candidates = set(left_axis)
                        placed_candidates.update(right_axis)
                        placed_candidates.update(to_append_left)
                        axis = [c for c in list_of_preferences[i] if c not in placed_candidates]
                        axis = to_append_left + left_axis + axis + right_axis
                        is_SP = is_single_peaked_axis(
                            instance, axis
                        )
                        end_flag = True
                        break

                    elif index_x_i > index_x > index_y > index_x_j:  # Case 2.(d)
                        placed_candidates = set(left_axis)
                        placed_candidates.update(right_axis)
                        placed_candidates.update(to_append_left)
                        axis = [c for c in list_of_preferences[i] if c not in placed_candidates]
                        axis.reverse()
                        axis = to_append_left + left_axis + axis + right_axis
                        is_SP = is_single_peaked_axis(
                            instance, axis
                        )
                        end_flag = True
                        break

                    elif index_x_i > index_x > index_x_j > index_y:  # Case 2.(c)
                        if forced_position.get(x, "") == "right" or forced_position.get(y, "") == "left":
                            end_flag = True
                            is_SP = False  # contradiction
                            break
                        forced_position[x] = "left"
                        forced_position[y] = "right"
                    elif index_x_j > index_x > index_x_i > index_y:  # Case 2.(c) Inverse
                        if forced_position.get(x, "") == "left" or forced_position.get(y, "") == "right":
                            end_flag = True
                            is_SP = False  # contradiction
                            break
                        forced_position[x] = "right"
                        forced_position[y] = "left"
                    elif index_x < index_x_i and index_x < index_x_j:  # Case 2.(b)
                        pass
                    else:
                        raise ValueError("We should never have ended up here with two "
                                         "candidates ranked last.")

                if not end_flag:
                    if x not in forced_position:
                        if y not in forced_position:
                            forced_position[x] = "left"
                            forced_position[y] = "right"
                        else:
                            forced_position[x] = "left" if forced_position[y] == "right" else "right"
                    if y not in forced_position:
                        forced_position[y] = "left" if forced_position[x] == "right" else "right"

                    if forced_position[x] == "left":
                        left_axis.append(x)
                        right_axis.insert(0, y)
                        x_i = x
                        x_j = y
                    else:
                        left_axis.append(y)
                        right_axis.insert(0, x)
                        x_i = y
                        x_j = x
    if is_SP:
        if axis is None:
            axis = left_axis + right_axis
        axis = to_append_left + axis
        return True, axis
    return False, None


def sp_cons_ones_matrix(instance, alt_map):
    """Returns a binary matrix such that the instance is single-peaked if and only if the matrix has the
    consecutive ones property. This is an helper function to implement the algorithm proposed by Bartholdi
    and Trick (1986) to deal with single-peakedness.

    :param instance: the instance to test for single-peakedness.
    :type instance: preflibtools.instances.preflibinstance.OrdinalInstance
    :param alt_map: a mapping from alternative name to range(0, m).
    :type alt_map: dict[_, int]

    :return: A binary matrix
    :rtype: numpy array
    """
    matrix = np.zeros((sum(len(o) for o in instance.orders), instance.num_alternatives))
    matrix_index = 0
    for order in instance.orders:
        for max_level in range(len(order)):
            for level_index in range(max_level + 1):
                level = order[level_index]
                for a in level:
                    matrix[matrix_index][alt_map[a]] = 1
            matrix_index += 1
    return matrix


def is_single_peaked_pq_tree(instance):
    if instance.data_type not in ("soc", "toc"):
        raise TypeError(
            "You are trying to test for single-peakedness on an instance of type "
            + str(instance.data_type)
            + ", this is not possible. Only toc and soc are allowed here."
        )

    alt_map = {n: k for k, n in enumerate(instance.alternatives_name)}
    matrix = sp_cons_ones_matrix(instance, alt_map)
    return isC1P(matrix)


def sp_ILP_trans_cstr(model, left_of_vars, instance):
    """A helper function for testing single-peakedness with an ILP solver. Adds the transitivity constraints to
    the ILP model given as parameter. These constraints encode that the axis constructed is transitive.

    :param model: The ILP model, should be an instance of the python-mip Model class.
    :param left_of_vars: A list of list of python-mip variables where leftOfVars[a1][a2] is set to 1 if and only
        if a1 is to the left of a2 in the axis.
    :param instance: the instance to test for single-peakedness.
    """
    for a1, a2, a3 in combinations(range(instance.num_alternatives), 3):
        model.add_constr(
            left_of_vars[a1][a2] + left_of_vars[a2][a3] - 1 <= left_of_vars[a1][a3],
            name="transitivity_" + str(a1) + "_" + str(a2) + "_" + str(a3),
        )
        model.add_constr(
            left_of_vars[a1][a3] + left_of_vars[a3][a2] - 1 <= left_of_vars[a1][a2],
            name="transitivity_" + str(a1) + "_" + str(a3) + "_" + str(a2),
        )
        model.add_constr(
            left_of_vars[a2][a1] + left_of_vars[a1][a3] - 1 <= left_of_vars[a2][a3],
            name="transitivity_" + str(a2) + "_" + str(a1) + "_" + str(a3),
        )
        model.add_constr(
            left_of_vars[a2][a3] + left_of_vars[a3][a1] - 1 <= left_of_vars[a2][a1],
            name="transitivity_" + str(a2) + "_" + str(a3) + "_" + str(a1),
        )
        model.add_constr(
            left_of_vars[a3][a1] + left_of_vars[a1][a2] - 1 <= left_of_vars[a3][a2],
            name="transitivity_" + str(a3) + "_" + str(a1) + "_" + str(a2),
        )
        model.add_constr(
            left_of_vars[a3][a2] + left_of_vars[a2][a1] - 1 <= left_of_vars[a3][a1],
            name="transitivity_" + str(a3) + "_" + str(a2) + "_" + str(a1),
        )


def sp_ILP_total_cstr(model, left_of_vars, instance):
    """A helper function for testing single-peakedness with an ILP solver. Adds the totality constraints to
    the ILP model given as parameter. These constraints encode that the axis constructed is total.

    :param model: The ILP model, should be an instance of the python-mip Model class.
    :param left_of_vars: A list of list of python-mip variables where leftOfVars[a1][a2] is set to 1 if and only
        if a1 is to the left of a2 in the axis.
    :param instance: the instance to test for single-peakedness.
    """
    for a1, a2 in combinations(range(instance.num_alternatives), 2):
        model.add_constr(
            left_of_vars[a1][a2] + left_of_vars[a2][a1] == 1,
            name="totality_" + str(a1) + "_" + str(a2),
        )


def sp_ILP_pos_cstr(model, left_of_vars, pos_vars, instance):
    """A helper function for testing single-peakedness with an ILP solver. Adds the position constraints to
    the ILP model given as parameter. These constraints enforce the position variables to follow the order
    defined by the left-of variables.

    :param model: The ILP model, should be an instance of the python-mip Model class.
    :param left_of_vars: A list of list of python-mip variables where leftOfVars[a1][a2] is set to 1 if and only
        if alternative a1 is to the left of alternative a2 in the axis.
    :param pos_vars: A list of list of python-mip variables where posVar[a1] indicates the position of
        alternative a1 in the axis.
    :param instance: the instance to test for single-peakedness.
    """
    num_alternatives = instance.num_alternatives
    for a1, a2 in combinations(range(num_alternatives), 2):
        model.add_constr(
            pos_vars[a1]
            <= pos_vars[a2] + num_alternatives * (1 - left_of_vars[a1][a2]),
            name="ordering_" + str(a1) + "_" + str(a2),
        )
        model.add_constr(
            pos_vars[a2] - pos_vars[a1]
            >= 0.5 * left_of_vars[a1][a2]
            - (1 - left_of_vars[a1][a2]) * num_alternatives,
            name="diffPos1_" + str(a1) + "_" + str(a2),
        )
        model.add_constr(
            pos_vars[a2]
            <= pos_vars[a1] + num_alternatives * (1 - left_of_vars[a2][a1]),
            name="ordering_" + str(a2) + "_" + str(a1),
        )
        model.add_constr(
            pos_vars[a1] - pos_vars[a2]
            >= 0.5 * left_of_vars[a2][a1]
            - (1 - left_of_vars[a2][a1]) * num_alternatives,
            name="diffPos1_" + str(a2) + "_" + str(a1),
        )


def sp_ILP_cons_ones_cstr(model, left_of_vars, instance, alt_map):
    """A helper function for testing single-peakedness with an ILP solver. Adds the single-peakedness constraints
    to the ILP model given as parameter. These constraints enforce that the instance is indeed single-peaked
    with respect to the axis constructed. They actually implement the consecutive ones property of the
    binary matrix corresponding to the instance.

    :param model: The ILP model, should be an instance of the python-mip Model class.
    :param left_of_vars: A list of list of python-mip variables where leftOfVars[a1][a2] is set to 1 if and only
        if a1 is to the left of a2 in the axis.
    :param instance: the instance to test for single-peakedness.
    :param alt_map: a mapping from alternative name to range(0, m).
    :type alt_map: dict[_, int]
    """
    matrix = sp_cons_ones_matrix(instance, alt_map)
    for row_index in range(len(matrix)):
        row = matrix[row_index]
        # print("Row{}: {}".format(rowIndex, row))
        zeros = set()
        ones = set()
        for index, value in enumerate(row):
            if value == 1:
                ones.add(index)
            else:
                zeros.add(index)
        for i, j in combinations(ones, 2):
            for k in zeros:
                model.add_constr(
                    left_of_vars[i][k] + left_of_vars[k][j] <= 1,
                    name=f"SP_row{row_index}_{i}_{j}_{k}"
                )
                model.add_constr(
                    left_of_vars[j][k] + left_of_vars[k][i] <= 1,
                    name=f"SP_row{row_index}_{j}_{i}_{k}"
                )


def sp_ILP_cons_ones_vot_del_cstr(model, left_of_vars, voter_vars, instance, alt_map):
    """A helper function for computing the closeness to single-peakedness of and instance with an ILP solver.
    Adds the single-peakedness constraints to the ILP model given as parameter, allowing to ignore some
    voters if needed. These constraints enforce that the instance is indeed single-peaked with respect to
    the axis constructed for the non-ignored voters. They actually implement the consecutive ones property of
    the binary matrix corresponding to the instance.

    :param model: The ILP model, should be an instance of the python-mip Model class.
    :param left_of_vars: A list of list of python-mip variables where leftOfVars[a1][a2] is set to 1 if and only
        if a1 is to the left of a2 in the axis.
    :param voter_vars: A list of list of python-mip variables where votersVars[v] is set to 1 if and only if
        voter v is removed from consideration.
    :param instance: the instance to test for single-peakedness.
    :type instance: preflibtools.instances.preflibinstance.OrdinalInstance
    :param alt_map: a mapping from alternative name to range(0, m).
    :type alt_map: dict[_, int]
    """
    matrix = sp_cons_ones_matrix(instance, alt_map)
    voter_index = -1
    for row_index in range(len(matrix)):
        row = matrix[row_index]
        if sum(row) == 1:
            voter_index += 1
        zeros = set()
        ones = set()
        for index, value in enumerate(row):
            if value == 1:
                ones.add(index)
            else:
                zeros.add(index)
        for i, j in combinations(ones, 2):
            for k in zeros:
                model.add_constr(
                    left_of_vars[i][k] + left_of_vars[k][j]
                    <= 1 + voter_vars[voter_index],
                    name=f"SP_row{row_index}_{i}_{j}_{k}"
                )
                model.add_constr(
                    left_of_vars[j][k] + left_of_vars[k][i]
                    <= 1 + voter_vars[voter_index],
                    name=f"SP_row{row_index}_{j}_{i}_{k}"
                )


def sp_ILP_cons_ones_alt_del_cstr(model, left_of_vars, alt_vars, instance, alt_map):
    """A helper function for computing the closeness to single-peakedness of and instance with an ILP solver.
    Adds the single-peakedness constraints to the ILP model given as parameter, allowing to ignore some
    alternatives if needed. These constraints enforce that the instance is indeed single-peaked with respect to
    the axis constructed for the non-ignored alternatives. They actually implement the consecutive ones property
    of the binary matrix corresponding to the instance.

    :param model: The ILP model, should be an instance of the python-mip Model class.
    :param left_of_vars: A list of list of python-mip variables where leftOfVars[a1][a2] is set to 1 if and only
        if a1 is to the left of a2 in the axis.
    :param alt_vars: A list of list of python-mip variables where altVars[a] is set to 1 if and only if
        alternative a is removed from consideration.
    :param instance: the instance to test for single-peakedness.
    :param alt_map: a mapping from alternative name to range(0, m).
    :type alt_map: dict[_, int]
    """
    matrix = sp_cons_ones_matrix(instance, alt_map)
    for row_index in range(len(matrix)):
        row = matrix[row_index]
        zeros = set()
        ones = set()
        for index, value in enumerate(row):
            if value == 1:
                ones.add(index)
            else:
                zeros.add(index)
        for i, j in combinations(ones, 2):
            for k in zeros:
                model.add_constr(
                    left_of_vars[i][k] + left_of_vars[k][j]
                    <= 1 + alt_vars[i] + alt_vars[j] + alt_vars[k],
                    name=f"SP_row{row_index}_{i}_{j}_{k}"
                )
                model.add_constr(
                    left_of_vars[j][k] + left_of_vars[k][i]
                    <= 1 + alt_vars[j] + alt_vars[i] + alt_vars[k],
                    name=f"SP_row{row_index}_{j}_{i}_{k}"
                )


def is_single_peaked_ILP(instance):
    """Tests whether the instance describes a profile of single-peaked preferences. It also works if indifference
    is allowed (the property would then be single-plateaued).

    This function implements the algorithm proposed by Bartholdi and Trick (1986). It first constructs the
    corresponding binary matrix and then uses an ILP solver to check whether the matrix has the consecutive
    ones property.

    This code is inspired by that of Zack Fitzsimmons (zfitzsim@holycross.edu) and Martin Lackner
    (lackner@dbai.tuwien.ac.at), available at https://github.com/zmf6921/incompletesp.

    :param instance: the instance to test for single-peakedness.
    :type instance: preflibtools.instances.preflibinstance.OrdinalInstance

    :return: A triple composed of a boolean variable indicating whether the instance is single-peaked or not,
        the python-mip optimisation status of the ILP model, and the axis for which the instance is single-peaked
        (None if the instance is not single-peaked).
    :rtype: Tuple(bool, str, list)
    """

    if instance.data_type not in ("toc", "soc"):
        raise TypeError(
            "You are trying to test for single-peakedness on an instance of type "
            + str(instance.data_type)
            + ", this is not possible. Only toc and soc are allowed here."
        )

    model = Model(sense=MINIMIZE)
    model.verbose = 0

    init_time = time.time()

    left_of_vars = np.array(
        [
            [
                model.add_var(var_type=BINARY, name="leftof_" + str(a1) + "_" + str(a2))
                for a2 in range(instance.num_alternatives)
            ]
            for a1 in range(instance.num_alternatives)
        ]
    )
    pos_vars = np.array(
        [
            model.add_var(
                var_type=INTEGER,
                name="pos_" + str(a),
                lb=1,
                ub=instance.num_alternatives,
            )
            for a in range(instance.num_alternatives)
        ]
    )

    alternatives_to_index = {a: i for i, a in enumerate(instance.alternatives_name)}
    index_to_alternatives = list(instance.alternatives_name)
    sp_ILP_trans_cstr(model, left_of_vars, instance)
    sp_ILP_total_cstr(model, left_of_vars, instance)
    sp_ILP_cons_ones_cstr(model, left_of_vars, instance, alternatives_to_index)
    sp_ILP_pos_cstr(model, left_of_vars, pos_vars, instance)

    model.objective = 0

    print(
        "Constraints for isSinglePeakedILP generated in {} seconds.".format(
            time.time() - init_time
        )
    )

    init_time = time.time()

    # model.write('modelSP.lp')

    model.max_gap = 0.05
    model.threads = -1
    opt_status = model.optimize()
    # if optStatus == OptimizationStatus.OPTIMAL:
    #     print('optimal solution cost {} found'.format(model.objective_value))
    # elif optStatus == OptimizationStatus.FEASIBLE:
    #     print('sol.cost {} found, best possible: {}'.format(model.objective_value, model.objective_bound))
    # elif optStatus == OptimizationStatus.NO_SOLUTION_FOUND:
    #     print('no feasible solution found, lower bound is: {}'.format(model.objective_bound))

    print("Solver is done, took {} seconds.".format(time.time() - init_time))

    if (
        opt_status == OptimizationStatus.OPTIMAL
        or opt_status == OptimizationStatus.FEASIBLE
    ):
        axis = [0 for _ in range(instance.num_alternatives)]
        for v in pos_vars:
            axis[int(v.x) - 1] = index_to_alternatives[int(v.name.split("_")[-1])]
        # print('solution:')
        # for v in model.vars:
        #     if abs(v.x) > 1e-6: # only printing non-zeros
        #         print('{} : {}'.format(v.name, v.x))
        return True, opt_status.name, axis
    return False, opt_status.name, None


def approx_SP_voter_deletion_ILP(instance, weighted=False):
    """Uses an ILP solver to compute how close to single-peakedness an instance, where closeness is measured as the
    smallest number of voter to remove for the instance to be single-peaked.

    :param instance: the instance to work on.
    :type instance: preflibtools.instances.preflibinstance.OrdinalInstance
    :param weighted: a boolean indicating if orders in the instance should have a weight of 1 in the ILP
        optimization (the default case), or if the weight should be the number of voters having submitted
        the order.

    :return: A quadruple composed of the number of voters that have been removed for the instance to be
        single-peaked, the python-mip optimisation status of the ILP model, the axis for which the instance
        is single-peaked, and the list of voters that have been removed.
    :rtype: Tuple(bool, str, list, list)
    """

    if instance.data_type not in ("toc", "soc"):
        raise TypeError(
            "You are trying to test for single-peakedness on an instance of type "
            + str(instance.data_type)
            + ", this is not possible. Only toc and soc are allowed here."
        )

    model = Model(sense=MINIMIZE)

    init_time = time.time()

    left_of_vars = np.array(
        [
            [
                model.add_var(var_type=BINARY, name="leftof_" + str(a1) + "_" + str(a2))
                for a2 in range(instance.num_alternatives)
            ]
            for a1 in range(instance.num_alternatives)
        ]
    )
    pos_vars = np.array(
        [
            model.add_var(
                var_type=INTEGER,
                name="pos_" + str(a),
                lb=1,
                ub=instance.num_alternatives,
            )
            for a in range(instance.num_alternatives)
        ]
    )
    voter_vars = np.array(
        [
            model.add_var(var_type=BINARY, name="delVoter_" + str(v))
            for v in range(len(instance.orders))
        ]
    )

    alternatives_to_index = {a: i for i, a in enumerate(instance.alternatives_name)}
    index_to_alternatives = list(instance.alternatives_name)
    sp_ILP_trans_cstr(model, left_of_vars, instance)
    print("Transitivity done")
    sp_ILP_total_cstr(model, left_of_vars, instance)
    print("Totality done")
    sp_ILP_cons_ones_vot_del_cstr(model, left_of_vars, voter_vars, instance, alternatives_to_index)
    print("Consecutive ones done")
    sp_ILP_pos_cstr(model, left_of_vars, pos_vars, instance)
    print("Position done")

    # model.start = [(v, 1) for v in votersVars[:-2]]

    if weighted:
        model.objective = xsum(
            v * instance.multiplicity[int(v.name.split("_")[-1])] for v in voter_vars
        )
    else:
        model.objective = xsum(v for v in voter_vars)

    print(
        "Constraints for approxSPVoterDeletionILP generated in {} seconds.".format(
            time.time() - init_time
        )
    )

    # model.write('modelSP.lp')

    # model.verbose = 0
    model.max_gap = 0.05
    model.threads = -1
    opt_status = model.optimize()
    # if optStatus == OptimizationStatus.OPTIMAL:
    #     print('optimal solution cost {} found'.format(model.objective_value))
    # elif optStatus == OptimizationStatus.FEASIBLE:
    #     print('sol.cost {} found, best possible: {}'.format(model.objective_value, model.objective_bound))
    # elif optStatus == OptimizationStatus.NO_SOLUTION_FOUND:
    #     print('no feasible solution found, lower bound is: {}'.format(model.objective_bound))

    print("Solver is done, took {} seconds.".format(time.time() - init_time))

    axis = None
    deleted_voters = None
    if (
        opt_status == OptimizationStatus.OPTIMAL
        or opt_status == OptimizationStatus.FEASIBLE
    ):
        axis = [0 for _ in range(instance.num_alternatives)]
        for v in pos_vars:
            axis[int(v.x) - 1] = index_to_alternatives[int(v.name.split("_")[-1])]
        deleted_voters = []
        for v in voter_vars:
            if v.x > 0:
                deleted_voters.append(v.name.split("_")[-1])
    #     print('solution:')
    #     for v in model.vars:
    #         if abs(v.x) > 1e-6: # only printing non-zeros
    #             print('{} : {}'.format(v.name, v.x))

    return model.objective_value, opt_status.name, axis, deleted_voters


def approx_SP_alternative_deletion_ILP(instance):
    """Uses an ILP solver to compute how close to single-peakedness an instance, where closeness is measured as the
    smallest number of alternatives to remove for the instance to be single-peaked.

    :param instance: the instance to work on.
    :type instance: preflibtools.instances.preflibinstance.OrdinalInstance

    :return: A quadruple composed of the number of alternatives that have been removed for the instance to be
        single-peaked, the python-mip optimisation status of the ILP model, the axis for which the instance
        is single-peaked, and the list of alternatives that have been removed.
    :rtype: Tuple(bool, str, list, list)
    """

    if instance.data_type not in ("toc", "soc"):
        raise TypeError(
            "You are trying to test for single-peakedness on an instance of type "
            + str(instance.data_type)
            + ", this is not possible. Only toc and soc are allowed here."
        )

    model = Model(sense=MINIMIZE)

    init_time = time.time()

    left_of_vars = np.array(
        [
            [
                model.add_var(var_type=BINARY, name="leftof_" + str(a1) + "_" + str(a2))
                for a2 in range(instance.num_alternatives)
            ]
            for a1 in range(instance.num_alternatives)
        ]
    )
    pos_vars = np.array(
        [
            model.add_var(
                var_type=INTEGER,
                name="pos_" + str(a),
                lb=1,
                ub=instance.num_alternatives,
            )
            for a in range(instance.num_alternatives)
        ]
    )
    alt_vars = np.array(
        [
            model.add_var(var_type=BINARY, name="delAlt_" + str(a))
            for a in range(instance.num_alternatives)
        ]
    )

    alternatives_to_index = {a: i for i, a in enumerate(instance.alternatives_name)}
    index_to_alternatives = list(instance.alternatives_name)
    sp_ILP_trans_cstr(model, left_of_vars, instance)
    sp_ILP_total_cstr(model, left_of_vars, instance)
    sp_ILP_cons_ones_alt_del_cstr(model, left_of_vars, alt_vars, instance, alternatives_to_index)
    sp_ILP_pos_cstr(model, left_of_vars, pos_vars, instance)

    model.start = [(a, 1) for a in alt_vars[:-2]]

    model.objective = xsum(a for a in alt_vars)

    print(
        "Constraints for approxSPAlternativeDeletionILP generated in {} seconds.".format(
            time.time() - init_time
        )
    )

    init_time = time.time()

    # model.write('modelSP.lp')

    # model.verbose = 0
    model.max_gap = 0.05
    model.threads = -1
    opt_status = model.optimize()
    # if optStatus == OptimizationStatus.OPTIMAL:
    #     print('optimal solution cost {} found'.format(model.objective_value))
    # elif optStatus == OptimizationStatus.FEASIBLE:
    #     print('sol.cost {} found, best possible: {}'.format(model.objective_value, model.objective_bound))
    # elif optStatus == OptimizationStatus.NO_SOLUTION_FOUND:
    #     print('no feasible solution found, lower bound is: {}'.format(model.objective_bound))

    print("Solver is done, took {} seconds.".format(time.time() - init_time))

    axis = None
    deleted_alts = None
    if (
        opt_status == OptimizationStatus.OPTIMAL
        or opt_status == OptimizationStatus.FEASIBLE
    ):
        axis = [0 for _ in range(instance.num_alternatives)]
        for v in pos_vars:
            axis[int(v.x) - 1] = index_to_alternatives[int(v.name.split("_")[-1])]
        deleted_alts = []
        for v in alt_vars:
            if v.x > 0:
                deleted_alts.append(v.name.split("_")[-1])
    #     print('solution:')
    #     for v in model.vars:
    #         if abs(v.x) > 1e-6: # only printing non-zeros
    #             print('{} : {}'.format(v.name, v.x))

    return model.objective_value, opt_status.name, axis, deleted_alts
