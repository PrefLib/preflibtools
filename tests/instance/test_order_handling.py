from unittest import TestCase

from preflibtools.instances import OrdinalInstance


class TestOrdinal(TestCase):
    def test_basic(self):
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
        instance.append_order_list(orders)
        assert instance.num_alternatives == 3
        assert instance.data_type == "soc"
        assert instance.num_voters == 2
        assert instance.orders == orders
        assert instance.multiplicity[((0,), (1,), (2,))] == 1
        assert instance.multiplicity[((2,), (0,), (1,))] == 1
        assert instance.flatten_strict() == [((0, 1, 2), 1), ((2, 0, 1), 1)]
        orders += [((0,), (1, 2))]
        instance.append_order_list(orders)
        assert instance.num_alternatives == 3
        assert instance.data_type == "toc"
        assert instance.num_voters == 5
        assert instance.multiplicity[((0,), (1,), (2,))] == 2
        assert instance.multiplicity[((2,), (0,), (1,))] == 2
        assert instance.multiplicity[((0,), (1, 2))] == 1
        orders += [((4, 3), (1, 2))]
        instance.append_order_list(orders)
        assert instance.num_alternatives == 5
        assert instance.data_type == "toi"
        assert instance.num_voters == 9
        assert instance.multiplicity[((0,), (1,), (2,))] == 3
        assert instance.multiplicity[((2,), (0,), (1,))] == 3
        assert instance.multiplicity[((0,), (1, 2))] == 2
        assert instance.multiplicity[((4, 3), (1, 2))] == 1
        instance.multiplicity[((4, 3), (1, 2))] += 10

        instance.recompute_cardinality_param()
        assert instance.num_voters == 19

    def test_vote_map(self):
        instance = OrdinalInstance()
        vote_map = {((0,), (1,), (2,)): 3, ((2,), (0,), (1,)): 2}
        instance.append_vote_map(vote_map)
        assert instance.num_alternatives == 3
        assert instance.data_type == "soc"
        assert instance.num_voters == 5
        assert len(instance.full_profile()) == 5
        assert instance.orders in (
            [((0,), (1,), (2,)), ((2,), (0,), (1,))],
            [((2,), (0,), (1,)), ((0,), (1,), (2,))],
        )
        vote_map = {
            ((0,), (1,), (2,)): 3,
            ((2,), (0,), (1,)): 2,
            ((0,), (1, 2)): 4,
            ((4, 3), (1, 2)): 2,
        }
        instance.append_vote_map(vote_map)
        assert instance.num_alternatives == 5
        assert instance.data_type == "toi"
        assert instance.num_voters == 16
        assert len(instance.full_profile()) == 16

        voteMapNew = instance.vote_map()
        assert voteMapNew[((0,), (1,), (2,))] == 6
        assert voteMapNew[((2,), (0,), (1,))] == 4
        assert voteMapNew[((0,), (1, 2))] == 4
        assert voteMapNew[((4, 3), (1, 2))] == 2
