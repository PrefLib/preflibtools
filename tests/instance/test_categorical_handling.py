from unittest import TestCase

from preflibtools.instances import OrdinalInstance, CategoricalInstance


class TestOrdinal(TestCase):

    def test_ordinal_to_cat(self):
        instance = OrdinalInstance()
        orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
        instance.append_order_list(orders)

        cat_instance = CategoricalInstance.from_ordinal(instance, size_truncators=[2])
        for p in cat_instance.preferences:
            assert len(p) == 2
            assert len(p[0]) == 2
        assert cat_instance.preferences[0][0] == (0, 1)
        assert cat_instance.preferences[0][1] == (2,)
        assert cat_instance.preferences[1][0] == (2, 0)
        assert cat_instance.preferences[1][1] == (1,)

        cat_instance = CategoricalInstance.from_ordinal(instance, relative_size_truncators=[0.4])
        for p in cat_instance.preferences:
            assert len(p) == 1
            assert len(p[0]) == 3
        cat_instance = CategoricalInstance.from_ordinal(instance, relative_size_truncators=[0.33, 0.33, 0.33])
        for p in cat_instance.preferences:
            assert len(p) == 3
            for cat in p:
                assert len(cat) == 1

        cat_instance = CategoricalInstance.from_ordinal(instance, num_indif_classes=[2])
        for p in cat_instance.preferences:
            assert len(p) == 2
            assert len(p[0]) == 2
        assert cat_instance.preferences[0][0] == (0, 1)
        assert cat_instance.preferences[0][1] == (2,)
        assert cat_instance.preferences[1][0] == (2, 0)
        assert cat_instance.preferences[1][1] == (1,)

        instance = OrdinalInstance()
        orders = [((0,), (1, 2)), ((4, 3), (1, 2))]
        instance.append_order_list(orders)
        cat_instance = CategoricalInstance.from_ordinal(instance, size_truncators=[2])
        assert len(cat_instance.preferences[0]) == 2
        assert cat_instance.preferences[0][0] == (0, 1, 2)
        assert len(cat_instance.preferences[0][1]) == 0
        assert len(cat_instance.preferences[1]) == 2
        assert cat_instance.preferences[1][0] == (4, 3)
        assert cat_instance.preferences[1][1] == (1, 2)

        cat_instance = CategoricalInstance.from_ordinal(instance, num_indif_classes=[2])
        assert len(cat_instance.preferences[0]) == 1
        assert cat_instance.preferences[0][0] == (0, 1, 2)
        assert len(cat_instance.preferences[1]) == 1
        assert cat_instance.preferences[1][0] == (4, 3, 1, 2)

        for _ in range(10):
            instance = OrdinalInstance()
            instance.populate_mallows_mix(30, 20, 4)
            cat_instance1 = CategoricalInstance.from_ordinal(instance, size_truncators=[5, 5, 4, 3, 3])
            cat_instance2 = CategoricalInstance.from_ordinal(instance,
                                                             relative_size_truncators=[0.25, 0.25, 0.2, 0.15, 0.15])
            assert cat_instance1.preferences == cat_instance2.preferences
            for p in cat_instance1.preferences:
                assert len(p) == cat_instance1.num_categories
            for p in cat_instance2.preferences:
                assert len(p) == cat_instance2.num_categories
