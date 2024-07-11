from preflibtools.instances.preflibinstance import OrdinalInstance

from unittest import TestCase

from preflibtools.properties.subdomains.ordinal.single_peaked.singlepeakedness import \
    is_single_peaked_axis, is_single_peaked, is_single_peaked_pq_tree, is_single_peaked_ILP, \
    approx_SP_voter_deletion_ILP, approx_SP_alternative_deletion_ILP


class TestAnalysis(TestCase):
    def test_single_peakedness(self):
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
        instance.append_order_list(orders)
        assert is_single_peaked_axis(instance, [0, 1, 2]) is False
        assert is_single_peaked_axis(instance, [1, 0, 2]) is True
        assert is_single_peaked(instance)[0] is True
        assert is_single_peaked_ILP(instance)[0] is True
        assert is_single_peaked_pq_tree(instance) is True

        instance = OrdinalInstance()
        orders = [
            ((0,), (1,), (2,)),
            ((2,), (1,), (0,)),
            ((1,), (0,), (2,)),
            ((1,), (2,), (0,)),
        ]
        instance.append_order_list(orders)
        assert is_single_peaked_axis(instance, [0, 1, 2]) is True
        assert is_single_peaked_axis(instance, [1, 0, 2]) is False
        assert is_single_peaked(instance)[0] is True
        assert is_single_peaked(instance)[1] in ([0, 1, 2], [2, 1, 0])
        assert is_single_peaked_ILP(instance)[0] is True
        assert is_single_peaked_ILP(instance)[2] in ([0, 1, 2], [2, 1, 0])
        assert is_single_peaked_pq_tree(instance) is True

        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (0,), (1,)), ((1,), (2,), (0,))]
        instance.append_order_list(orders)
        assert is_single_peaked(instance)[0] is False
        assert is_single_peaked_ILP(instance)[0] is False
        assert is_single_peaked_pq_tree(instance) is False
        assert approx_SP_voter_deletion_ILP(instance)[0] == 1
        assert approx_SP_alternative_deletion_ILP(instance)[0] == 1

        instance = OrdinalInstance()
        orders = [
            ((0, 1), (2,), (3, 4)),
            ((4,), (3,), (2, 1, 0)),
            ((2, 3), (1,), (0,), (4,)),
        ]
        instance.append_order_list(orders)
        assert is_single_peaked_ILP(instance)[0] is True
        assert is_single_peaked_pq_tree(instance) is True
        assert approx_SP_voter_deletion_ILP(instance)[0] == 0
        assert approx_SP_alternative_deletion_ILP(instance)[0] == 0

        instance = OrdinalInstance()
        instance.populate_mallows_mix(30, 7, 5)
        is_single_peaked_ILP(instance)
        approx_SP_voter_deletion_ILP(instance)
        approx_SP_alternative_deletion_ILP(instance)
