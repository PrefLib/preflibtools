from preflibtools.properties.subdomains.ordinal.single_peaked.k_axes import two_axes_sp
from preflibtools.instances.sampling import prefsampling_ordinal_wrapper

from preflibtools.properties.subdomains.ordinal.single_peaked.singlepeakedness import is_single_peaked
from preflibtools.instances import OrdinalInstance

from prefsampling.ordinal import k_axes_single_peaked

from unittest import TestCase


class TestKAxesSinglePeaked(TestCase):
    def test_2_axes_single_peaked(self):

        # test 1, sp profile
        params = {
            "num_voters" : 200,
            "num_candidates" : 11,
            "k": 1,
            "axes_weights": 0.5,
            "seed" : 1
        }
        vote_map = prefsampling_ordinal_wrapper(k_axes_single_peaked, params)
        instance = OrdinalInstance()
        instance.append_vote_map(vote_map)

        is_2SP, partitions = two_axes_sp(instance)

        assert is_2SP
        
        first = OrdinalInstance()
        first.append_order_array(partitions[0])
        assert is_single_peaked(first)[0]

        assert len(partitions[1]) == 0

        # test 2, 2-axes sp
        params = {
            "num_voters" : 200,
            "num_candidates" : 11,
            "k" : 2,
            "axes_weights": 0.5,
            "seed" : 10
        }
        vote_map = prefsampling_ordinal_wrapper(k_axes_single_peaked, params)
        instance = OrdinalInstance()
        instance.append_vote_map(vote_map)

        is_2SP, partitions = two_axes_sp(instance)
        assert is_2SP

        first = OrdinalInstance()
        first.append_order_array(partitions[0])
        assert is_single_peaked(first)[0]

        second = OrdinalInstance()
        second.append_order_array(partitions[1])
        assert is_single_peaked(second)[0]
