from preflibtools.properties.subdomains.ordinal.single_peaked.k_alternative_partition import generate_k_alt_partition_sp, k_alternative_partition_DFS
from preflibtools.instances.sampling import prefsampling_ordinal_wrapper

from preflibtools.instances import OrdinalInstance

from unittest import TestCase


class Testanalysis(TestCase):
    def test_alt_partition_single_peaked(self):

        # test 1, sp profile
        params = {
            "num_voters": 400,
            "partitions": [11],
            "seed": 2
        }
        vote_map = prefsampling_ordinal_wrapper(generate_k_alt_partition_sp, params)
        instance = OrdinalInstance()
        instance.append_vote_map(vote_map)

        partitions = k_alternative_partition_DFS(instance, 5)

        assert len(partitions) == 1

        # test 2, non-sp profile, 5 partitions
        params = {
            "num_voters": 400,
            "partitions": [6, 3, 2, 4, 1],
            "seed": 2
        }
        vote_map = prefsampling_ordinal_wrapper(generate_k_alt_partition_sp, params)
        instance = OrdinalInstance()
        instance.append_vote_map(vote_map)


        partitions = k_alternative_partition_DFS(instance, 7)

        assert len(partitions) == 5
        
        # test 3, non-sp profile, 7 partitions 
        params = {
            "num_voters": 400,
            "partitions": [7, 2, 2, 2, 5, 2, 1],
            "seed": 5
        }
        vote_map = prefsampling_ordinal_wrapper(generate_k_alt_partition_sp, params)
        instance = OrdinalInstance()
        instance.append_vote_map(vote_map)

        partitions = k_alternative_partition_DFS(instance, 8)

        assert len(partitions) == 7
