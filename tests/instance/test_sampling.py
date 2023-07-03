from unittest import TestCase

from preflibtools.instances import OrdinalInstance


class TestSampling(TestCase):

    def test_IC(self):
        instance = OrdinalInstance()
        instance.populate_IC(5, 10)
        assert instance.num_voters == 5
        assert instance.num_alternatives == 10

        instance = OrdinalInstance()
        instance.populate_IC_anon(5, 10)
        assert instance.num_voters == 5
        assert instance.num_alternatives == 10

    def test_urn(self):
        instance = OrdinalInstance()
        instance.populate_urn(5, 10, 76)
        assert instance.num_voters == 5
        assert instance.num_alternatives == 10

        instance = OrdinalInstance()
        with self.assertRaises(ValueError):
            instance.populate_urn(10, 30, 2)

        instance = OrdinalInstance()
        instance.populate_urn(30, 10, 2)
        assert instance.num_voters == 30
        assert instance.num_alternatives == 10

        instance = OrdinalInstance()
        instance.populate_urn(30, 2, 2)
        assert instance.num_voters == 30
        assert sum(instance.multiplicity.values()) == 30
        assert instance.num_alternatives == 2

    def test_mallows(self):
        instance = OrdinalInstance()
        instance.populate_mallows(5, 3, [0.4, 0.6], [0.2, 0.3], [((0,), (1,), (2,)), ((1,), (0,), (2,))])
        assert instance.num_voters == 5
        assert instance.num_alternatives == 3

        instance = OrdinalInstance()
        instance.populate_mallows(5, 3, [10, 20], [0.2, 0.3], [((0,), (1,), (2,)), ((1,), (0,), (2,))])
        assert instance.num_voters == 5
        assert instance.num_alternatives == 3

        instance = OrdinalInstance()
        instance.populate_mallows_mix(5, 10, 5)
        assert instance.num_voters == 5
        assert instance.num_alternatives == 10

        instance = OrdinalInstance()
        with self.assertRaises(ValueError):
            instance.populate_mallows(5, 3, [0.4, 0.6, 0.7], [0.2, 0.3], [((0,), (1,), (2,)), ((1,), (0,), (2,))])

        instance = OrdinalInstance()
        with self.assertRaises(ValueError):
            instance.populate_mallows(5, 3, [0.4, 0.6], [0.2, 0.3, 0.4], [((0,), (1,), (2,)), ((1,), (0,), (2,))])

        instance = OrdinalInstance()
        with self.assertRaises(ValueError):
            instance.populate_mallows(5, 3, [0.4, 0.6], [0.2, 0.3], [((0,), (1,), (2,)), ((1,), (0,), (2,)),
                                                                     ((0,), (2,), (1,))])
            