from preflibtools.properties.subdomains.ordinal.single_peaked.k_alternative_deletion import generate_k_alt_nearly_sp, k_alternative_deletion, remove_alternatives
from preflibtools.instances.sampling import prefsampling_ordinal_wrapper

from preflibtools.properties.subdomains.ordinal.single_peaked.singlepeakedness import is_single_peaked
from preflibtools.instances import OrdinalInstance

from unittest import TestCase


class Testanalysis(TestCase):
    def test_alt_deletion_single_peaked(self):

        # test 1, sp profile
        params = {
            "num_voters" : 500,
            "num_alternatives" : 11,
            "k": 0,
            "seed" : 1
        }
        vote_map = prefsampling_ordinal_wrapper(generate_k_alt_nearly_sp, params)
        instance = OrdinalInstance()
        instance.append_vote_map(vote_map)

        axis, candidates = k_alternative_deletion(instance)
        SP_instance = remove_alternatives(instance, candidates)

        assert axis == [i for i in range(11)]
        assert candidates == []
        assert is_single_peaked(SP_instance)

        # test 2, non-sp profile, remove 4 
        params = {
            "num_voters" : 500,
            "num_alternatives" : 11,
            "k" : 4,
            "seed" : 10
        }
        vote_map = prefsampling_ordinal_wrapper(generate_k_alt_nearly_sp, params)
        instance = OrdinalInstance()
        instance.append_vote_map(vote_map)


        axis, candidates = k_alternative_deletion(instance)
        SP_instance = remove_alternatives(instance, candidates)

        assert len(axis) == 7
        assert len(candidates) == 4
        assert is_single_peaked(SP_instance)

        # test 3, non-sp profile, remove 7 
        params = {
            "num_voters" : 10000,
            "num_alternatives" : 12,
            "k" : 7,
            "seed" : 5
        }
        vote_map = prefsampling_ordinal_wrapper(generate_k_alt_nearly_sp, params)
        instance = OrdinalInstance()
        instance.append_vote_map(vote_map)

        axis, candidates = k_alternative_deletion(instance)
        SP_instance = remove_alternatives(instance, candidates)

        assert len(axis) == 5
        assert len(candidates) == 7
        assert is_single_peaked(SP_instance)