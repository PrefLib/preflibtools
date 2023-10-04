from preflibtools.instances.preflibinstance import OrdinalInstance
from preflibtools.aggregation import *

from unittest import TestCase


class TestAnalysis(TestCase):
    def test_borda(self):
        # 0 > 1 > 2
        # 2 > 0 > 1
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
        instance.append_order_list(orders)
        scores = borda_scores(instance)
        assert scores[0] == 3
        assert scores[1] == 1
        assert scores[2] == 2
    
    def test_condorcet_not_exists(self):
        # 0 > 1 > 2
        # 2 > 0 > 1
        # 1 > 2 > 0
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (0,), (1,)), ((1,), (2,), (0,))]
        instance.append_order_list(orders)
        assert has_condorcet(instance) is False
    
    def test_condorcet_exists(self):
        # 0 > 1 > 2
        # 2 > 1 > 0
        # 1 > 0 > 2
        # 1 > 2 > 0
        instance = OrdinalInstance()
        orders = [
            ((0,), (1,), (2,)),
            ((2,), (1,), (0,)),
            ((1,), (0,), (2,)),
            ((1,), (2,), (0,)),
        ]
        instance.append_order_list(orders)
        assert has_condorcet(instance) is True
