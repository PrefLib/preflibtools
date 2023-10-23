from preflibtools.instances.preflibinstance import OrdinalInstance
from preflibtools.properties import *

from unittest import TestCase


class TestAnalysis(TestCase):
    
    def test_distance(self):
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
        instance.append_order_list(orders)
        distance_matrix(instance, kendall_tau_distance)
        distance_matrix(instance, spearman_footrule_distance)
        distance_matrix(instance, sertel_distance)
