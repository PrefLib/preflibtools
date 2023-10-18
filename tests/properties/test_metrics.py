from preflibtools.instances.preflibinstance import OrdinalInstance
from preflibtools.properties import *

from unittest import TestCase


class TestAnalysis(TestCase):

    def test_pairwise_scores_strict(self):
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)),
                  ((0,), (1,), (2,)),
                  ((2,), (1,), (0,))]
        instance.append_order_list(orders)
        scores = pairwise_scores(instance)
        assert scores[0][1] == 2
        assert scores[1][0] == 1
        assert scores[1][2] == 2
    
    def test_pairwise_scores_tied(self):
        instance = OrdinalInstance()
        orders = [((0,), (1,2)),
                  ((0,), (1,), (2,)),
                  ((2,), (1,0))]
        instance.append_order_list(orders)
        scores = pairwise_scores(instance)
        assert scores[0][1] == 2
        assert scores[1][0] == 0
        assert scores[1][2] == 1
    
    def test_copeland_strict(self):
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)),
                  ((0,), (1,), (2,)),
                  ((2,), (1,), (0,))]
        instance.append_order_list(orders)
        scores = copeland_scores(instance)
        assert scores[0][1] == 1
        assert scores[1][0] == -1
        assert scores[1][2] == 1

    def test_copeland_ties(self):
        instance = OrdinalInstance()
        orders = [((0,3), (1,), (2,)),
                  ((0,), (1,2), (3,)),
                  ((2,), (1,), (0,), (3,))]
        instance.append_order_list(orders)
        scores = copeland_scores(instance)
        assert scores[0][1] == 1
        assert scores[3][0] == -2
        assert scores[1][2] == 0

    def test_has_weak_condorcet_true(self):
        instance = OrdinalInstance()
        orders = [
            ((0,), (1,), (2,)),
            ((2,), (1,), (0,)),
        ]
        instance.append_order_list(orders)
        assert has_condorcet(instance, weak_condorcet=True) is True

    def test_has_weak_condorcet_false(self):
        instance = OrdinalInstance()
        orders = [
            ((0,), (1,), (2,)),
            ((2,), (0,), (1,)),
            ((1,), (2,), (0,)),
        ]
        instance.append_order_list(orders)
        assert has_condorcet(instance, weak_condorcet=True) is False

    def test_has_condorcet_false(self):
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (0,), (1,)), ((1,), (2,), (0,))]
        instance.append_order_list(orders)
        assert has_condorcet(instance) is False

    def test_has_condorcet_true(self):
        instance = OrdinalInstance()
        orders = [
            ((0,), (1,), (2,)),
            ((2,), (1,), (0,)),
            ((1,), (0,), (2,)),
            ((1,), (2,), (0,)),
        ]
        instance.append_order_list(orders)
        assert has_condorcet(instance) is True

    def test_borda_strict(self):
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
        instance.append_order_list(orders)
        scores = borda_scores(instance)
        assert scores[0] == 3
        assert scores[1] == 1
        assert scores[2] == 2
    
    def test_borda_ties(self):
        instance = OrdinalInstance()
        orders = [((0,2), (1,)), ((2,), (0,), (1,))]
        instance.append_order_list(orders)
        scores = borda_scores(instance)
        assert scores[0] == 2
        assert scores[1] == 0
        assert scores[2] == 3
