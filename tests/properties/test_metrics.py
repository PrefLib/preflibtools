from preflibtools.instances.preflibinstance import OrdinalInstance
from preflibtools.properties.metrics import *

from unittest import TestCase


class TestAnalysis(TestCase):

    def test_borda(self):
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
        instance.append_order_list(orders)
        scores = borda_scores(instance)
        assert scores[0] == 3
        assert scores[1] == 1
        assert scores[2] == 2
        orders += [((0,), (1, 2))]
        instance.append_order_list(orders)
        scores = borda_scores(instance)
        assert scores[0] == 8
        assert scores[1] == 2
        assert scores[2] == 4
        
    def test_condorcet():
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (0,), (1,)), ((1,), (2,), (0,))]
        instance.append_order_list(orders)
        assert has_condorcet(instance) is False
        instance = OrdinalInstance()
        orders = [
            ((0,), (1,), (2,)),
            ((2,), (1,), (0,)),
            ((1,), (0,), (2,)),
            ((1,), (2,), (0,)),
        ]
        instance.append_order_list(orders)
        assert has_condorcet(instance) is True
        instance = OrdinalInstance()
        orders = [
            ((0,), (1,), (2,)),
            ((2,), (1,), (0,)),
        ]
        instance.append_order_list(orders)
        assert has_condorcet(instance) is False
        assert has_condorcet(instance, weak_condorcet=True) is True
        instance = OrdinalInstance()
        orders = [((0, 1), (2,), (3, 4)), ((4,), (3,), (2, 1, 0)), ((0,), (1, 3), (4,))]
        instance.append_order_list(orders)
        assert has_condorcet(instance) is True
