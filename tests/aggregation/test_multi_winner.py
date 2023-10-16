from preflibtools.instances.preflibinstance import OrdinalInstance
from preflibtools.aggregation.utilities import *
from preflibtools.aggregation.single_winner import *
from preflibtools.aggregation.multi_winner import *

from unittest import TestCase
import pytest


class TestApprovalChamberlinCourant:
    def test_approval_cc(self):
        instance = OrdinalInstance()
        orders = [
            ((0,),(1,2,3)),
            ((2,3),(1,0)),
            ((2,0),(1,3)),
            ((0,1,3),(2,))
            ]
        instance.append_order_list(orders)
        assert approval_chamberlin_courant_committee(instance, 2) == [{0,2},{0,3}]
 

class TestBordalChamberlinCourant:
    def test_borda_cc(self):
        instance = OrdinalInstance()
        orders = [
            ((0,),(2,),(1,),(3,)),
            ((1,),(0,),(2,),(3,)),
            ((3,),(0,),(2,),(1,)),
            ]
        instance.append_order_list(orders)
        assert borda_chamberlin_courant_committee(instance, 2) == [{0,1},{0,3}]