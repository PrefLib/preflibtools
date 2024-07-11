from preflibtools.properties.subdomains.ordinal.single_peaked.k_axes import generate_k_axes_sp, two_axes_sp
from preflibtools.instances.sampling import prefsampling_ordinal_wrapper

from preflibtools.properties.subdomains.ordinal.single_peaked.singlepeakedness import is_single_peaked
from preflibtools.instances import OrdinalInstance

from unittest import TestCase


class Testanalysis(TestCase):
    def test_2_axes_single_peaked(self):

        # test 1, sp profile
        params = {
            "num_voters_partition" : 200,
            "num_alternatives" : 11,
            "k": 1,
            "seed" : 1
        }
        vote_map = prefsampling_ordinal_wrapper(generate_k_axes_sp, params)
        instance = OrdinalInstance()
        instance.append_vote_map(vote_map)

        is_2SP, partitions = two_axes_sp(instance)

        assert is_2SP
        print(is_2SP)
        
        first = OrdinalInstance()
        first.append_order_array(partitions[0])
        assert is_single_peaked(first)[0]

        assert len(partitions[1]) == 0

        # test 2, 2-axes sp
        params = {
            "num_voters_partition" : 200,
            "num_alternatives" : 7,
            "k" : 2,
            "seed" : 10
        }
        vote_map = prefsampling_ordinal_wrapper(generate_k_axes_sp, params)
        instance = OrdinalInstance()
        instance.append_vote_map(vote_map)


        is_2SP, partitions = two_axes_sp(instance)
        print(is_2SP)

        assert is_2SP

        first = OrdinalInstance()
        first.append_order_array(partitions[0])
        assert is_single_peaked(first)[0]

        second = OrdinalInstance()
        second.append_order_array(partitions[1])
        assert is_single_peaked(second)[0]

        # test 3, >2-axes single-peaked
        params = {
            "num_voters_partition" : 300,
            "num_alternatives" : 8,
            "k" : 4,
            "seed" : 5
        }
        vote_map = prefsampling_ordinal_wrapper(generate_k_axes_sp, params)
        instance = OrdinalInstance()
        instance.append_vote_map(vote_map)

        is_2SP, partitions = two_axes_sp(instance)

        assert not is_2SP
        print(is_2SP)
