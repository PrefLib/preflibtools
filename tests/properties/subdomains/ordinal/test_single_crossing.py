from prefsampling.ordinal import single_crossing

from preflibtools.instances.preflibinstance import OrdinalInstance

from unittest import TestCase

from preflibtools.instances.sampling import prefsampling_ordinal_wrapper
from preflibtools.properties.subdomains.ordinal.singlecrossing import is_single_crossing, \
    is_single_crossing_conflict_sets

import time

class TestSingleCrossing(TestCase):
    def test_single_crossing_positive(self):

        for seed in range(50):
            params = {
                "num_voters": 200,
                "num_candidates": 30,
                "seed": seed
            }
            print(seed)
            vote_map = prefsampling_ordinal_wrapper(single_crossing, params)
            print(vote_map)
            instance = OrdinalInstance()
            instance.append_vote_map(vote_map)
            print(instance)

            is_sc_conflict_sets = is_single_crossing_conflict_sets(instance)
            assert is_sc_conflict_sets
            print(is_sc_conflict_sets)

            is_sc, sc_orders = is_single_crossing(instance)
            assert is_sc
            print(is_sc)
