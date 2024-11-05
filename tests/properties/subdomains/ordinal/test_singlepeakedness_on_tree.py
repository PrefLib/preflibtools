from prefsampling.ordinal import single_peaked_conitzer, single_peaked_walsh

from preflibtools.instances.preflibinstance import OrdinalInstance

from unittest import TestCase

from preflibtools.instances.sampling import prefsampling_ordinal_wrapper
from preflibtools.properties.subdomains.ordinal.singlepeaked.single_peaked_tree import \
    is_single_peaked_on_tree

class TestSinglePeakedTree(TestCase):
    def test_single_peakedness_tree(self):
        for seed in range(50):
            for sampler in [single_peaked_conitzer, single_peaked_walsh]:
                params = {
                    "num_voters": 2000,
                    "num_candidates": 30,
                    "seed": seed
                }
                vote_map = prefsampling_ordinal_wrapper(sampler, params)
                instance = OrdinalInstance()
                instance.append_vote_map(vote_map)

                is_sp, order = is_single_peaked_on_tree(instance)
                assert is_sp
