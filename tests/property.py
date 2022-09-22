from preflibtools.instances.preflibinstance import OrdinalInstance
from preflibtools.properties.singlepeakedness import *
from preflibtools.properties.singlecrossing import *
from preflibtools.properties.distances import *
from preflibtools.properties import *


def test_basic():
    instance = OrdinalInstance()
    orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
    instance.append_order_list(orders)
    scores = borda_scores(instance)
    assert scores[0] == 3
    assert scores[1] == 1
    assert scores[2] == 2
    assert num_alternatives(instance) == 3
    assert num_voters(instance) == 2
    assert num_different_preferences(instance) == 2
    assert largest_ballot(instance) == 3
    assert smallest_ballot(instance) == 3
    assert max_num_indif(instance) == 0
    assert min_num_indif(instance) == 0
    assert largest_indif(instance) == 1
    assert smallest_indif(instance) == 1
    assert is_approval(instance) is False
    assert is_strict(instance) is True
    assert is_complete(instance) is True
    orders += [((0,), (1, 2))]
    instance.append_order_list(orders)
    scores = borda_scores(instance)
    assert scores[0] == 8
    assert scores[1] == 2
    assert scores[2] == 4
    assert num_alternatives(instance) == 3
    assert num_voters(instance) == 5
    assert num_different_preferences(instance) == 3
    assert largest_ballot(instance) == 3
    assert smallest_ballot(instance) == 3
    assert max_num_indif(instance) == 1
    assert min_num_indif(instance) == 0
    assert largest_indif(instance) == 2
    assert smallest_indif(instance) == 1
    assert is_approval(instance) is False
    assert is_strict(instance) is False
    assert is_complete(instance) is True
    orders += [((4, 3), (1, 2))]
    instance.append_order_list(orders)
    assert num_alternatives(instance) == 5
    assert num_voters(instance) == 9
    assert num_different_preferences(instance) == 4
    assert largest_ballot(instance) == 4
    assert smallest_ballot(instance) == 3
    assert max_num_indif(instance) == 2
    assert min_num_indif(instance) == 0
    assert largest_indif(instance) == 2
    assert smallest_indif(instance) == 1
    assert is_approval(instance) is False
    assert is_strict(instance) is False
    assert is_complete(instance) is False

    instance = OrdinalInstance()
    instance.append_order_list([((4, 3), (1, 2)), ((1, 3), (1, 4))])
    assert is_approval(instance) is True
    instance.append_order_list([((2, 3), (1,)), ((3,), (1, 2))])
    assert is_approval(instance) is False

    instance = OrdinalInstance()
    instance.append_order_list([((2, 3),), ((3,),)])
    assert is_approval(instance) is True

    instance = OrdinalInstance()
    orders = [((0,), (1,), (2,)), ((2,), (0,), (1,)), ((1,), (2,), (0,))]
    instance.append_order_list(orders)
    assert has_condorcet(instance) is False
    instance = OrdinalInstance()
    orders = [((0,), (1,), (2,)), ((2,), (1,), (0,)), ((1,), (0,), (2,)), ((1,), (2,), (0,))]
    instance.append_order_list(orders)
    assert has_condorcet(instance) is True
    instance = OrdinalInstance()
    orders = [((0, 1), (2,), (3, 4)), ((4,), (3,), (2, 1, 0)), ((0,), (1, 3), (4,))]
    instance.append_order_list(orders)
    assert has_condorcet(instance) is True


def single_peakedness_test():
    instance = OrdinalInstance()
    orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
    instance.append_order_list(orders)
    assert is_single_peaked_axis(instance, [0, 1, 2]) is False
    assert is_single_peaked_axis(instance, [1, 0, 2]) is True
    assert is_single_peaked(instance)[0] is True
    assert is_single_peaked_ILP(instance)[0] is True

    instance = OrdinalInstance()
    orders = [((0,), (1,), (2,)), ((2,), (1,), (0,)), ((1,), (0,), (2,)), ((1,), (2,), (0,))]
    instance.append_order_list(orders)
    assert is_single_peaked_axis(instance, [0, 1, 2]) is True
    assert is_single_peaked_axis(instance, [1, 0, 2]) is False
    assert is_single_peaked(instance)[0] is True
    assert is_single_peaked(instance)[1] in ([0, 1, 2], [2, 1, 0])
    assert is_single_peaked_ILP(instance)[0] is True
    assert is_single_peaked_ILP(instance)[2] in ([0, 1, 2], [2, 1, 0])

    instance = OrdinalInstance()
    orders = [((0,), (1,), (2,)), ((2,), (0,), (1,)), ((1,), (2,), (0,))]
    instance.append_order_list(orders)
    assert is_single_peaked(instance)[0] is False
    assert is_single_peaked_ILP(instance)[0] is False
    assert approx_SP_voter_deletion_ILP(instance)[0] == 1
    assert approx_SP_alternative_deletion_ILP(instance)[0] == 1

    instance = OrdinalInstance()
    orders = [((0, 1), (2,), (3, 4)), ((4,), (3,), (2, 1, 0)), ((2, 3), (1,), (0,), (4,))]
    instance.append_order_list(orders)
    assert is_single_peaked_ILP(instance)[0] is True
    assert approx_SP_voter_deletion_ILP(instance)[0] == 0
    assert approx_SP_alternative_deletion_ILP(instance)[0] == 0

    instance = OrdinalInstance()
    instance.populate_mallows_mix(30, 7, 5)
    is_single_peaked_ILP(instance)
    approx_SP_voter_deletion_ILP(instance)
    approx_SP_alternative_deletion_ILP(instance)


def single_crossing_test():
    instance = OrdinalInstance()
    orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
    instance.append_order_list(orders)
    is_single_crossing(instance)


def distance_test():
    instance = OrdinalInstance()
    orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
    instance.append_order_list(orders)
    distance_matrix(instance, kendall_tau_distance)
    distance_matrix(instance, spearman_footrule_distance)
    distance_matrix(instance, sertel_distance)


def main():
    print("Test basic...")
    test_basic()
    print("Test single-peakedness...")
    single_peakedness_test()
    print("Test single-crossing...")
    single_crossing_test()
    print("Test distances...")
    distance_test()
    print("All tests successful")


if __name__ == "__main__":
    main()
