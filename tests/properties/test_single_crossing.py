from preflibtools.instances.preflibinstance import OrdinalInstance
from preflibtools.properties.singlecrossing import *

from unittest import TestCase


class TestAnalysis(TestCase):

    def test_single_crossing(self):
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
        instance.append_order_list(orders)
        is_single_crossing(instance)
