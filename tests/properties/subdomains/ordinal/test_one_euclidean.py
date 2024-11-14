from prefsampling import EuclideanSpace
from prefsampling.ordinal import euclidean

from preflibtools.instances.preflibinstance import OrdinalInstance

from unittest import TestCase

from preflibtools.instances.sampling import prefsampling_ordinal_wrapper
from preflibtools.properties.subdomains.ordinal.euclidean import is_one_euclidean


class TestOrdinalEuclidean(TestCase):
    def test_one_euclidean_positive(self):

        for seed in range(50):
            params = {
                "num_voters": 500,
                "num_candidates": 30,
                "num_dimensions": 1,
                "voters_positions": EuclideanSpace.UNIFORM_SPHERE,
                "candidates_positions": EuclideanSpace.GAUSSIAN_CUBE,
            }
            vote_map = prefsampling_ordinal_wrapper(euclidean, params)
            instance = OrdinalInstance()
            instance.append_vote_map(vote_map)

            is_euclidean, mapping = is_one_euclidean(instance)
            assert is_euclidean
