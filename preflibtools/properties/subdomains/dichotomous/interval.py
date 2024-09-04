import numpy as np

from preflibtools.properties.subdomains.consecutive_ones import solve_consecutive_ones


def instance_to_ci_matrix(instance):
    """
    Builds a matrix so that the instance is candidate interval if and only if the matrix has the
    consecutive ones property.

    :param instance: the instance, only the first class is used
    :type instance: preflibtools.instances.preflibinstance.CategoricalInstance
    """
    alternatives = list(instance.alternatives_name)
    matrix = np.zeros((len(instance.preferences), instance.num_alternatives), dtype=int)
    for idx, vote in enumerate(instance.preferences):
        for alt in vote[0]:
            matrix[idx][alternatives.index(alt)] = 1
    return matrix


def is_candidate_interval(instance):
    """
    Tests whether the given categorical instance is candidate interval.

    :param instance: the instance
    :type instance: CategoricalInstance

    :return: A tuple consisting of a boolean indicating if the instance is candidate interval and
        the ordering of the candidates (or None if the instance is not candidate interval).
    :rtype: tuple[bool, list | None]
    """
    matrix = instance_to_ci_matrix(instance)
    res, ordered_idx = solve_consecutive_ones(matrix)
    if res:
        alternative_names = list(instance.alternatives_name)
        candidates_order = [alternative_names[i] for i in ordered_idx]
        return True, candidates_order
    return False, None


def is_candidate_extremal_interval(instance):
    """
    Tests whether the given categorical instance is candidate extremal interval.

    :param instance: the instance
    :type instance: CategoricalInstance

    :return: A tuple consisting of a boolean indicating if the instance is candidate extremal
        interval and the ordering of the candidates (or None if the instance is not
        candidate extremal interval).
    :rtype: tuple[bool, list | None]
    """
    matrix = instance_to_ci_matrix(instance)
    complement_matrix = 1 - matrix
    final_matrix = np.vstack((matrix, complement_matrix))
    res, ordered_idx = solve_consecutive_ones(final_matrix)
    if res:
        alternative_names = list(instance.alternatives_name)
        candidate_order = [alternative_names[i] for i in ordered_idx[:len(alternative_names)]]
        return True, candidate_order
    return False, None


def is_voter_interval(instance):
    """
    Tests whether the given categorical instance is voter interval.

    :param instance: the instance
    :type instance: CategoricalInstance

    :return: A tuple consisting of a boolean indicating if the instance is voter interval and
        the ordering of the voters (or None if the instance is not voter interval).
    :rtype: tuple[bool, list | None]
    """
    matrix = instance_to_ci_matrix(instance)
    transposed_matrix = np.transpose(matrix)
    return solve_consecutive_ones(transposed_matrix)


def is_voter_extremal_interval(instance):
    """
    Tests whether the given categorical instance is voter extremal interval.

    :param instance: the instance
    :type instance: CategoricalInstance

    :return: A tuple consisting of a boolean indicating if the instance is voter extremal interval
        and the ordering of the voters (or None if the instance is not voter extremal interval).
    :rtype: tuple[bool, list | None]
    """
    matrix = instance_to_ci_matrix(instance)
    transposed_matrix = np.transpose(matrix)
    complement_matrix = 1 - transposed_matrix
    final_matrix = np.vstack((transposed_matrix, complement_matrix))
    return solve_consecutive_ones(final_matrix)
