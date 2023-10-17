from preflibtools.instances.preflibinstance import OrdinalInstance
from preflibtools.properties.basic import *

from unittest import TestCase


class TestAnalysis(TestCase):
    def test_ordinal(self):
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
        instance.append_order_list(orders)
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

    def test_approval():
        instance = OrdinalInstance()
        instance.append_order_list([((4, 3), (1, 2)), ((1, 3), (1, 4))])
        assert is_approval(instance) is True
        instance.append_order_list([((2, 3), (1,)), ((3,), (1, 2))])
        assert is_approval(instance) is False
