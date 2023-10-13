from preflibtools.instances.preflibinstance import OrdinalInstance
from preflibtools.aggregation.utilities import *
from preflibtools.aggregation.single_winner import *

from unittest import TestCase
import pytest


class TestPlurality:
    def test_plurality_only_one_winner(self):
        instance = OrdinalInstance()
        orders = [
            ((0,), (1,2)),
            ((2,), (0,), (1,)),
            ((2,), (0,2)),
            ((1,), (0,), (2,))
            ]
        instance.append_order_list(orders)
        assert plurality_winner(instance) == {2}
    
    def test_plurality_multiple_winner(self):
        instance = OrdinalInstance()
        orders = [
            ((0,), (1,), (2,)),
            ((0,), (1,), (2,)),
            ((2,), (0,), (1,)),
            ((2,), (0,), (1,)),
            ((1,), (0,), (2,))
            ]
        instance.append_order_list(orders)
        assert plurality_winner(instance) == {2,0}


class TestKApproval:
    def test_k_approval(self):
        instance = OrdinalInstance()
        orders = [
            ((0,), (1,), (2,), (3,)),
            ((3,), (1,), (0,), (2,)),
            ((2,), (0,), (1,), (3,)),
            ((0,), (1,), (2,), (3,))
            ]
        instance.append_order_list(orders)
        assert k_approval_winner(instance, 2) == {0, 1}


class TestBorda:
    def test_borda_only_one_winner(self):
        instance = OrdinalInstance()
        orders = [
            ((0,), (1,), (2,)),
            ((2,), (0,), (1,)),
            ((1,), (0,), (2,))
            ]
        instance.append_order_list(orders)
        assert borda_winner(instance) == {0}
    
    def test_borda_multiple_winner(self):
        instance = OrdinalInstance()
        orders = [
            ((0,), (1,), (2,)),
            ((0,), (1,), (2,)),
            ((1,), (0,), (2,)),
            ((1,), (0,), (2,))
            ]
        instance.append_order_list(orders)
        assert borda_winner(instance) == {1,0}


class TestCopeland:
    def test_copeland_condorcet_winner(self):
        instance = OrdinalInstance()
        orders = [
            ((0,), (1,), (2,)),
            ((2,), (0,), (1,)),
            ((0,), (1,), (2,))
            ]
        instance.append_order_list(orders)
        assert copeland_winner(instance) == {0}
    
    def test_copeland_condorcet_cycle(self):
        instance = OrdinalInstance()
        orders = [
            ((0,), (1,), (2,)),
            ((2,), (0,), (1,)),
            ((1,), (2,), (0,))
            ]
        instance.append_order_list(orders)
        assert copeland_winner(instance) == {0, 1, 2}


class TestApproval:
    def test_approval_winner(self):
        instance = OrdinalInstance()
        orders = [
            ((0,1),),
            ((2,),),
            ((2,3),)
            ]
        instance.append_order_list(orders)
        assert approval_winner(instance) == {2}

    def test_approval_winner2(self):
        instance = OrdinalInstance()
        orders = [
            ((0,1),(2,3)),
            ((2,),(0,1,3)),
            ((2,3),(0,1))
            ]
        instance.append_order_list(orders)
        assert approval_winner(instance) == {2}

class TestSatisfactionApproval:
    def test_satisfaction_approval_winner(self):
        instance = OrdinalInstance()
        orders = [
            ((1,2,3),),
            ((0,),),
            ((2,3),)
            ]
        instance.append_order_list(orders)
        assert satisfaction_approval_winner(instance) == {0}
