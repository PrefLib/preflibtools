from prefsampling.ordinal import single_crossing

from preflibtools.instances.preflibinstance import OrdinalInstance

from unittest import TestCase

from preflibtools.instances.sampling import prefsampling_ordinal_wrapper
from preflibtools.properties.subdomains.ordinal.singlecrossing import (
    is_single_crossing,
    is_single_crossing_conflict_sets,
)


class TestSingleCrossing(TestCase):
    def test_single_crossing_positive(self):
        for seed in range(50):
            params = {"num_voters": 500, "num_candidates": 30, "seed": seed}
            vote_map = prefsampling_ordinal_wrapper(single_crossing, params)
            instance = OrdinalInstance()
            instance.append_vote_map(vote_map)

            is_sc, sc_orders = is_single_crossing(instance)
            assert is_sc

    def test_single_crossing_conflict_sets_positive(self):
        for seed in range(50):
            params = {"num_voters": 200, "num_candidates": 10, "seed": seed}
            vote_map = prefsampling_ordinal_wrapper(single_crossing, params)
            instance = OrdinalInstance()
            instance.append_vote_map(vote_map)

            is_sc = is_single_crossing_conflict_sets(instance)
            assert is_sc
