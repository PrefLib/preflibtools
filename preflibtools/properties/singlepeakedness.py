""" This module provides procedures to deal with the potential single-peakedness of the instance.
"""

import copy
import time

from itertools import combinations
from mip import *


def is_single_peaked_axis(instance, axis):
    """ Tests whether the instance is single-peaked with respect to the axis provided as argument.

        :param instance: the instance to work on.
        :type instance: preflibtools.instance.preflibinstance.OrdinalInstance
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
        raise TypeError("You are trying to test for single-peakedness on an instance of type " +
                        str(instance.data_type) + ", this is not possible. Only toc and soc are allowed here.")

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
    """ Tests whether the instance describes a profile of single-peaked preferences. It only works with strict
        preferences.

        This function implements the algorithm of Escoffier, Lang, and Ozturk (2008). We are grateful to Thor Yung 
        Pheng who developed this function (under the supervision of Umberto Grandi).

        :param instance: the instance to test for single-peakedness.
        :type instance: preflibtools.instance.preflibinstance.OrdinalInstance

        :return: The axis with respect to which the instance would be single-peaked, the empty list if the instance
            is not single-peaked.
        :rtype: list
    """

    if instance.data_type != "soc":
        raise TypeError("You are trying to use the algorithm of Escoffier, Lang, and Ozturk (2008) to test single-" +
                        "peakedness on an instance of type " + str(instance.data_type) + ", this is not possible.")

    is_SP = True
    end_flag = False
    axis = None
    right_axis, left_axis = [], []
    x_i, x_j = None, None

    # generates list of preferences without the weight while flattening the orders
    list_of_preferences = [list(orderMultiplicity[0]) for orderMultiplicity in instance.flatten_strict()]

    # list_of_preferences_SP: list to modify
    list_of_preferences_SP = copy.deepcopy(list_of_preferences)

    iteration = 0
    while is_SP and len(list_of_preferences_SP[0]) >= 1 and not end_flag:

        # make a list of last candidates
        last_candidates = []
        for preference in list_of_preferences_SP:
            last_candidate = preference.pop()
            if last_candidate not in last_candidates:
                last_candidates.append(last_candidate)

        if len(last_candidates) >= 3:  # impossible to position all candidates in leftmost and rightmost axis
            is_SP = False
            end_flag = True

        elif len(last_candidates) == 1:
            x = last_candidates[0]
            for preference in list_of_preferences_SP:
                if x in preference:
                    preference.remove(x)

            case = 0

            for i in range(len(list_of_preferences)):

                # find index of x, x_i, x_j in each preference
                index_x = list_of_preferences[i].index(x)
                if x_i is None:
                    index_x_i = -1
                else:
                    index_x_i = list_of_preferences[i].index(x_i)
                if x_j is None:
                    index_x_j = -1
                else:
                    index_x_j = list_of_preferences[i].index(x_j)

                # 3 possibilities for len(last_candidates) == 1
                if index_x_i > index_x > index_x_j:  # Case 1
                    case_i = 1
                    if case == 0:
                        case = case_i
                    elif case == 1:
                        pass
                    elif case == 2:
                        end_flag = True
                        is_SP = False  # contradiction
                        break
                elif index_x_j > index_x > index_x_j:  # Case 2
                    case_i = 2
                    if case == 0:
                        case = case_i
                    elif case == 2:
                        pass
                    elif case == 1:
                        end_flag = True
                        is_SP = False  # contradiction
                        break
                elif index_x > index_x_i and index_x > index_x_j:  # Case 0
                    case_i = 0

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
            x = last_candidates[0]
            y = last_candidates[1]
            for preference in list_of_preferences_SP:
                if x in preference:
                    preference.remove(x)
                if y in preference:
                    preference.remove(y)

            case = 0

            for i in range(len(list_of_preferences)):

                # find index of x, y, x_i, x_j in each preference
                index_x = list_of_preferences[i].index(x)
                index_y = list_of_preferences[i].index(y)

                if x_i is None:
                    index_x_i = -1
                else:
                    index_x_i = list_of_preferences[i].index(x_i)
                if x_j is None:
                    index_x_j = -1
                else:
                    index_x_j = list_of_preferences[i].index(x_j)

                # swap position to put x in the lower position (ranked last)
                if index_y > index_x:
                    index_x, index_y = index_y, index_x

                # all possible cases
                if index_x_i > index_x > index_y > index_x_j or index_x_j > index_x > index_y > index_x_i:  # Case 4
                    case_i = 4

                    # get index for leftover elements and append them into left axis following increasing order
                    T_bar = last_candidates + list_of_preferences_SP[i]
                    order = []
                    for candidate in T_bar:
                        index_candidate = list_of_preferences[i].index(candidate)
                        order.append((index_candidate, candidate))
                    order.sort(reverse=True)
                    for index, candidate in order:
                        left_axis.append(candidate)

                    axis = left_axis + right_axis

                    is_SP = is_single_peaked_axis(instance, axis)  # to be completed , complete right n left axis
                    end_flag = True
                    break

                elif index_x_i > index_x > index_x_j > index_y:  # Case 1
                    case_i = 1
                    if case == 0:
                        case = case_i
                    elif case == 1:
                        pass
                    elif case == 2:
                        end_flag = True
                        is_SP = False  # contradiction
                        break
                elif index_x_j > index_x > index_x_i > index_y:  # Case 2
                    case_i = 2
                    if case == 0:
                        case = case_i
                    elif case == 2:
                        pass
                    elif case == 1:
                        end_flag = True
                        is_SP = False  # contradiction
                        break
                elif index_x > index_x_i and index_x > index_x_j:
                    case_i = 0

                    # add x and y  in leftmost or rightmost axis according to case if axis is compatible

            if not end_flag:
                if case == 0:
                    left_axis.append(x)
                    right_axis.insert(0, y)
                    x_i = x
                    x_j = y
                elif case == 1:
                    left_axis.append(x)
                    right_axis.insert(0, y)
                    x_i = x
                    x_j = y
                elif case == 2:
                    left_axis.append(y)
                    right_axis.insert(0, x)
                    x_i = y
                    x_j = x

        iteration += 1

    if is_SP and axis is None:
        axis = left_axis + right_axis

    return is_SP, axis


def sp_cons_ones_matrix(instance):
    """ Returns a binary matrix such that the instance is single-peaked if and only if the matrix has the 
        consecutive ones property. This is an helper function to implement the algorithm proposed by Bartholdi 
        and Trick (1986) to deal with single-peakedness.

        :param instance: the instance to test for single-peakedness.
        :type instance: preflibtools.instance.preflibinstance.OrdinalInstance

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
                    matrix[matrix_index][a] = 1
            matrix_index += 1
    return matrix


def sp_ILP_trans_cstr(model, left_of_vars, instance):
    """ A helper function for testing single-peakedness with an ILP solver. Adds the transitivity constraints to 
        the ILP model given as parameter. These constraints encode that the axis constructed is transitive.

        :param model: The ILP model, should be an instance of the python-mip Model class.
        :param left_of_vars: A list of list of python-mip variables where leftOfVars[a1][a2] is set to 1 if and only
            if a1 is to the left of a2 in the axis.
        :param instance: the instance to test for single-peakedness.
    """
    for (a1, a2, a3) in combinations(range(instance.num_alternatives), 3):
        model.add_constr(left_of_vars[a1][a2] + left_of_vars[a2][a3] - 1 <= left_of_vars[a1][a3],
                         name="transitivity_" + str(a1) + "_" + str(a2) + "_" + str(a3))
        model.add_constr(left_of_vars[a1][a3] + left_of_vars[a3][a2] - 1 <= left_of_vars[a1][a2],
                         name="transitivity_" + str(a1) + "_" + str(a3) + "_" + str(a2))
        model.add_constr(left_of_vars[a2][a1] + left_of_vars[a1][a3] - 1 <= left_of_vars[a2][a3],
                         name="transitivity_" + str(a2) + "_" + str(a1) + "_" + str(a3))
        model.add_constr(left_of_vars[a2][a3] + left_of_vars[a3][a1] - 1 <= left_of_vars[a2][a1],
                         name="transitivity_" + str(a2) + "_" + str(a3) + "_" + str(a1))
        model.add_constr(left_of_vars[a3][a1] + left_of_vars[a1][a2] - 1 <= left_of_vars[a3][a2],
                         name="transitivity_" + str(a3) + "_" + str(a1) + "_" + str(a2))
        model.add_constr(left_of_vars[a3][a2] + left_of_vars[a2][a1] - 1 <= left_of_vars[a3][a1],
                         name="transitivity_" + str(a3) + "_" + str(a2) + "_" + str(a1))


def sp_ILP_total_cstr(model, left_of_vars, instance):
    """ A helper function for testing single-peakedness with an ILP solver. Adds the totality constraints to 
        the ILP model given as parameter. These constraints encode that the axis constructed is total.

        :param model: The ILP model, should be an instance of the python-mip Model class.
        :param left_of_vars: A list of list of python-mip variables where leftOfVars[a1][a2] is set to 1 if and only
            if a1 is to the left of a2 in the axis.
        :param instance: the instance to test for single-peakedness.
    """
    for (a1, a2) in combinations(range(instance.num_alternatives), 2):
        model.add_constr(left_of_vars[a1][a2] + left_of_vars[a2][a1] == 1, name="totality_" + str(a1) + "_" + str(a2))


def sp_ILP_pos_cstr(model, left_of_vars, pos_vars, instance):
    """ A helper function for testing single-peakedness with an ILP solver. Adds the position constraints to 
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
    for (a1, a2) in combinations(range(num_alternatives), 2):
        model.add_constr(pos_vars[a1] <= pos_vars[a2] + num_alternatives * (1 - left_of_vars[a1][a2]),
                         name="ordering_" + str(a1) + "_" + str(a2))
        model.add_constr(pos_vars[a2] - pos_vars[a1] >= 0.5 * left_of_vars[a1][a2] - (1 - left_of_vars[a1][a2]) * num_alternatives,
                         name="diffPos1_" + str(a1) + "_" + str(a2))
        model.add_constr(pos_vars[a2] <= pos_vars[a1] + num_alternatives * (1 - left_of_vars[a2][a1]),
                         name="ordering_" + str(a2) + "_" + str(a1))
        model.add_constr(pos_vars[a1] - pos_vars[a2] >= 0.5 * left_of_vars[a2][a1] - (1 - left_of_vars[a2][a1]) * num_alternatives,
                         name="diffPos1_" + str(a2) + "_" + str(a1))


def sp_ILP_cons_ones_cstr(model, left_of_vars, instance):
    """ A helper function for testing single-peakedness with an ILP solver. Adds the single-peakedness constraints 
        to the ILP model given as parameter. These constraints enforce that the instance is indeed single-peaked
        with respect to the axis constructed. They actually implement the consecutive ones property of the 
        binary matrix corresponding to the instance. 

        :param model: The ILP model, should be an instance of the python-mip Model class.
        :param left_of_vars: A list of list of python-mip variables where leftOfVars[a1][a2] is set to 1 if and only
            if a1 is to the left of a2 in the axis.
        :param instance: the instance to test for single-peakedness.
    """
    matrix = sp_cons_ones_matrix(instance)
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
        for (i, j) in combinations(ones, 2):
            for k in zeros:
                model.add_constr(left_of_vars[i][k] + left_of_vars[k][j] <= 1,
                                 name="SP_row" + str(row_index) + "_" + str(i) + "_" + str(j) + "_" + str(k))
                model.add_constr(left_of_vars[j][k] + left_of_vars[k][i] <= 1,
                                 name="SP_row" + str(row_index) + "_" + str(j) + "_" + str(i) + "_" + str(k))


def sp_ILP_cons_ones_vot_del_cstr(model, left_of_vars, voter_vars, instance):
    """ A helper function for computing the closeness to single-peakedness of and instance with an ILP solver. 
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
        :type instance: preflibtools.instance.preflibinstance.OrdinalInstance
    """
    matrix = sp_cons_ones_matrix(instance)
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
        for (i, j) in combinations(ones, 2):
            for k in zeros:
                model.add_constr(left_of_vars[i][k] + left_of_vars[k][j] <= 1 + voter_vars[voter_index],
                                 name="SP_row" + str(row_index) + "_" + str(i) + "_" + str(j) + "_" + str(k))
                model.add_constr(left_of_vars[j][k] + left_of_vars[k][i] <= 1 + voter_vars[voter_index],
                                 name="SP_row" + str(row_index) + "_" + str(j) + "_" + str(i) + "_" + str(k))


def sp_ILP_cons_ones_alt_del_cstr(model, left_of_vars, alt_vars, instance):
    """ A helper function for computing the closeness to single-peakedness of and instance with an ILP solver. 
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
    """
    matrix = sp_cons_ones_matrix(instance)
    for row_index in range(len(matrix)):
        row = matrix[row_index]
        zeros = set()
        ones = set()
        for index, value in enumerate(row):
            if value == 1:
                ones.add(index)
            else:
                zeros.add(index)
        for (i, j) in combinations(ones, 2):
            for k in zeros:
                model.add_constr(left_of_vars[i][k] + left_of_vars[k][j] <= 1 + alt_vars[i] + alt_vars[j] + alt_vars[k],
                                 name="SP_row" + str(row_index) + "_" + str(i) + "_" + str(j) + "_" + str(k))
                model.add_constr(left_of_vars[j][k] + left_of_vars[k][i] <= 1 + alt_vars[j] + alt_vars[i] + alt_vars[k],
                                 name="SP_row" + str(row_index) + "_" + str(j) + "_" + str(i) + "_" + str(k))


def is_single_peaked_ILP(instance):
    """ Tests whether the instance describes a profile of single-peaked preferences. It also works if indifference
        is allowed (the property would then be single-plateaued).

        This function implements the algorithm proposed by Bartholdi and Trick (1986). It first constructs the 
        corresponding binary matrix and then uses an ILP solver to check whether the matrix has the consecutive 
        ones property.

        This code is inspired by that of Zack Fitzsimmons (zfitzsim@holycross.edu) and Martin Lackner 
        (lackner@dbai.tuwien.ac.at), available at https://github.com/zmf6921/incompletesp.

        :param instance: the instance to test for single-peakedness.
        :type instance: preflibtools.instance.preflibinstance.OrdinalInstance

        :return: A triple composed of a boolean variable indicating whether the instance is single-peaked or not, 
            the python-mip optimisation status of the ILP model, and the axis for which the instance is single-peaked
            (None if the instance is not single-peaked).
        :rtype: Tuple(bool, str, list)
    """

    if instance.data_type not in ("toc", "soc"):
        raise TypeError("You are trying to test for single-peakedness on an instance of type " +
                        str(instance.data_type) + ", this is not possible. Only toc and soc are allowed here.")

    model = Model(sense=MINIMIZE)

    init_time = time.time()

    left_of_vars = np.array([[model.add_var(var_type=BINARY,
                                          name='leftof_' + str(a1) + '_' + str(a2)) for a2 in
                            range(instance.num_alternatives)] for a1 in range(instance.num_alternatives)])
    pos_vars = np.array([model.add_var(var_type=INTEGER,
                                      name='pos_' + str(a), lb=1, ub=instance.num_alternatives) for a in
                        range(instance.num_alternatives)])

    sp_ILP_trans_cstr(model, left_of_vars, instance)
    sp_ILP_total_cstr(model, left_of_vars, instance)
    sp_ILP_cons_ones_cstr(model, left_of_vars, instance)
    sp_ILP_pos_cstr(model, left_of_vars, pos_vars, instance)

    model.objective = 0

    print("Constraints for isSinglePeakedILP generated in {} seconds.".format(time.time() - init_time))

    init_time = time.time()

    # model.write('modelSP.lp')

    model.verbose = 0
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

    if opt_status == OptimizationStatus.OPTIMAL or opt_status == OptimizationStatus.FEASIBLE:
        axis = [0 for i in range(instance.num_alternatives)]
        for v in pos_vars:
            axis[int(v.x) - 1] = int(v.name.split("_")[-1])
        # print('solution:')
        # for v in model.vars:
        #     if abs(v.x) > 1e-6: # only printing non-zeros
        #         print('{} : {}'.format(v.name, v.x))
        return True, opt_status.name, axis
    return False, opt_status.name, None


def approx_SP_voter_deletion_ILP(instance, weighted=False):
    """ Uses an ILP solver to compute how close to single-peakedness an instance, where closeness is measured as the 
        smallest number of voter to remove for the instance to be single-peaked.

        :param instance: the instance to work on.
        :type instance: preflibtools.instance.preflibinstance.OrdinalInstance
        :param weighted: a boolean indicating if orders in the instance should have a weight of 1 in the ILP
            optimization (the default case), or if the weight should be the number of voters having submitted
            the order. 

        :return: A quadruple composed of the number of voters that have been removed for the instance to be
            single-peaked, the python-mip optimisation status of the ILP model, the axis for which the instance 
            is single-peaked, and the list of voters that have been removed.
        :rtype: Tuple(bool, str, list, list)
    """

    if instance.data_type not in ("toc", "soc"):
        raise TypeError("You are trying to test for single-peakedness on an instance of type " +
                        str(instance.data_type) + ", this is not possible. Only toc and soc are allowed here.")

    model = Model(sense=MINIMIZE)

    init_time = time.time()

    left_of_vars = np.array([[model.add_var(var_type=BINARY, name='leftof_' + str(a1) + '_' + str(a2)) for a2 in
                            range(instance.num_alternatives)] for a1 in range(instance.num_alternatives)])
    pos_vars = np.array(
        [model.add_var(var_type=INTEGER, name='pos_' + str(a), lb=1, ub=instance.num_alternatives) for a in
         range(instance.num_alternatives)])
    voter_vars = np.array(
        [model.add_var(var_type=BINARY, name='delVoter_' + str(v)) for v in range(len(instance.orders))])

    sp_ILP_trans_cstr(model, left_of_vars, instance)
    print("Transitivity done")
    sp_ILP_total_cstr(model, left_of_vars, instance)
    print("Totality done")
    sp_ILP_cons_ones_vot_del_cstr(model, left_of_vars, voter_vars, instance)
    print("Consecutive ones done")
    sp_ILP_pos_cstr(model, left_of_vars, pos_vars, instance)
    print("Position done")

    # model.start = [(v, 1) for v in votersVars[:-2]]

    if weighted:
        model.objective = xsum(v * instance.multiplicity[int(v.name.split('_')[-1])] for v in voter_vars)
    else:
        model.objective = xsum(v for v in voter_vars)

    print("Constraints for approxSPVoterDeletionILP generated in {} seconds.".format(time.time() - init_time))

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
    if opt_status == OptimizationStatus.OPTIMAL or opt_status == OptimizationStatus.FEASIBLE:
        axis = [0 for i in range(instance.num_alternatives)]
        for v in pos_vars:
            axis[int(v.x) - 1] = int(v.name.split("_")[-1])
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
    """ Uses an ILP solver to compute how close to single-peakedness an instance, where closeness is measured as the 
        smallest number of alternatives to remove for the instance to be single-peaked.

        :param instance: the instance to work on.
        :type instance: preflibtools.instance.preflibinstance.OrdinalInstance

        :return: A quadruple composed of the number of alternatives that have been removed for the instance to be
            single-peaked, the python-mip optimisation status of the ILP model, the axis for which the instance 
            is single-peaked, and the list of alternatives that have been removed.
        :rtype: Tuple(bool, str, list, list)
    """

    if instance.data_type not in ("toc", "soc"):
        raise TypeError("You are trying to test for single-peakedness on an instance of type " +
                        str(instance.data_type) + ", this is not possible. Only toc and soc are allowed here.")

    model = Model(sense=MINIMIZE)

    init_time = time.time()

    left_of_vars= np.array([[model.add_var(var_type=BINARY, name='leftof_' + str(a1) + '_' + str(a2)) for a2 in
                            range(instance.num_alternatives)] for a1 in range(instance.num_alternatives)])
    pos_vars = np.array(
        [model.add_var(var_type=INTEGER, name='pos_' + str(a), lb=1, ub=instance.num_alternatives) for a in
         range(instance.num_alternatives)])
    alt_vars = np.array(
        [model.add_var(var_type=BINARY, name='delAlt_' + str(a)) for a in range(instance.num_alternatives)])

    sp_ILP_trans_cstr(model, left_of_vars, instance)
    sp_ILP_total_cstr(model, left_of_vars, instance)
    sp_ILP_cons_ones_alt_del_cstr(model, left_of_vars, alt_vars, instance)
    sp_ILP_pos_cstr(model, left_of_vars, pos_vars, instance)

    model.start = [(a, 1) for a in alt_vars[:-2]]

    model.objective = xsum(a for a in alt_vars)

    print("Constraints for approxSPAlternativeDeletionILP generated in {} seconds.".format(time.time() - init_time))

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
    if opt_status == OptimizationStatus.OPTIMAL or opt_status == OptimizationStatus.FEASIBLE:
        axis = [0 for i in range(instance.num_alternatives)]
        for v in pos_vars:
            axis[int(v.x) - 1] = int(v.name.split("_")[-1])
        deleted_alts = []
        for v in alt_vars:
            if v.x > 0:
                deleted_alts.append(v.name.split("_")[-1])
    #     print('solution:')
    #     for v in model.vars:
    #         if abs(v.x) > 1e-6: # only printing non-zeros
    #             print('{} : {}'.format(v.name, v.x))

    return model.objective_value, opt_status.name, axis, deleted_alts
