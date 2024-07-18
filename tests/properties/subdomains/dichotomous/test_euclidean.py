import unittest
import random
from prefsampling import EuclideanSpace
from prefsampling.approval import euclidean_vcr
from itertools import combinations

from properties.subdomains.dichotomous.euclidean import is_dichotomous_uniformly_euclidean
from tests.properties.subdomains.dichotomous.partition_tests import generate_PART_instances
from tests.properties.subdomains.dichotomous.test_interval import generate_cei_instances, \
    generate_vei_instances, generate_not_ci_instances, generate_not_cei_instances_tucker_1, \
    generate_not_cei_instances_tucker_2, generate_not_cei_instances_tucker_4, \
    generate_not_cei_instances_tucker_5, generate_not_cei_instances_tucker_3
from tests.properties.subdomains.dichotomous.test_singlecrossing import generate_WSC_instance, \
    generate_NOT_WSC_instance


class TestDUE(unittest.TestCase):

    def test_positive_examples_due_prefsampling(self):
        for _ in range(100):
            a = random.randint(5, 50)
            v = random.randint(5, 50)
            instance = euclidean_vcr(
                num_voters=v, num_candidates=a,
                voters_radius=1 / a, candidates_radius=1 / a,
                num_dimensions=1,
                voters_positions=EuclideanSpace.UNIFORM_BALL,
                candidates_positions=EuclideanSpace.UNIFORM_BALL
            )
            res, _ = is_dichotomous_uniformly_euclidean(instance)
            self.assertTrue(res or res is None)

    def test_negative_examples_due_prefsampling_added_votes(self):
        for _ in range(100):
            a = random.randint(5, 50)
            v = random.randint(5, 50)
            instance = euclidean_vcr(
                num_voters=v, num_candidates=a,
                voters_radius=1 / a, candidates_radius=1 / a,
                num_dimensions=1,
                voters_positions=EuclideanSpace.UNIFORM_BALL,
                candidates_positions=EuclideanSpace.UNIFORM_BALL
            )
            vote = {i for i in range(a)}
            instance.append(vote)
            for i in range(a):
                vote = {i}
                instance.append(vote)
            res, _ = is_dichotomous_uniformly_euclidean(instance)
            self.assertTrue(not res or res is None)

    def test_positive_examples_due_wsc(self):
        for _ in range(100):
            a = random.randint(10, 20)
            alternatives = [i for i in range(a)]
            v = random.randint(5, len(list(combinations(alternatives, 2))))
            instance = generate_WSC_instance(a, v)
            res, _ = is_dichotomous_uniformly_euclidean(instance)
            self.assertTrue(res or res is None)

    def test_negative_examples_due_wsc(self):
        for _ in range(100):
            a = random.randint(10, 20)
            alternatives = [i for i in range(a)]
            v = random.randint(5, len(list(combinations(alternatives, 2))))
            instance = generate_NOT_WSC_instance(a, v)
            res, _ = is_dichotomous_uniformly_euclidean(instance)
            self.assertTrue(not res or res is None)

    def test_positive_examples_due_cei(self):
        for _ in range(1):
            a = random.randint(5, 100)
            v = random.randint(5, 100)
            instance = generate_cei_instances(a, v)
            res, _ = is_dichotomous_uniformly_euclidean(instance)
            self.assertTrue(res)

    def test_positive_examples_due_vei(self):
        for _ in range(1):
            a = random.randint(5, 100)
            v = random.randint(5, 100)
            instance = generate_vei_instances(a, v)
            res, _ = is_dichotomous_uniformly_euclidean(instance)
            self.assertTrue(res)

    def test_positive_examples_due_part(self):
        for _ in range(1):
            a = random.randint(5, 100)
            v = random.randint(5, 100)
            instance = generate_PART_instances(a, v)
            res, _ = is_dichotomous_uniformly_euclidean(instance)
            self.assertTrue(res)

    def test_negative_examples_due_not_ci(self):
        for _ in range(10):
            a = random.randint(5, 30)
            v = random.randint(5, 100)
            instance = generate_not_ci_instances(a, v)
            res, _ = is_dichotomous_uniformly_euclidean(instance)
            self.assertTrue(not res)

    def test_negative_examples_due_t1(self):
        for _ in range(10):
            a = random.randint(5, 30)
            instance = generate_not_cei_instances_tucker_1(a)
            res, _ = is_dichotomous_uniformly_euclidean(instance)
            self.assertTrue(not res)

    def test_negative_examples_due_t2(self):
        for _ in range(10):
            a = random.randint(5, 30)
            instance = generate_not_cei_instances_tucker_2(a)
            res, _ = is_dichotomous_uniformly_euclidean(instance)
            self.assertTrue(not res)

    def test_negative_examples_due_t3(self):
        for _ in range(10):
            a = random.randint(5, 30)
            instance = generate_not_cei_instances_tucker_3(a)
            res, _ = is_dichotomous_uniformly_euclidean(instance)
            self.assertTrue(not res)

    def test_negative_examples_due_t4(self):
        instance = generate_not_cei_instances_tucker_4()
        res, _ = is_dichotomous_uniformly_euclidean(instance)
        self.assertTrue(not res)

    def test_negative_examples_due_t5(self):
        instance = generate_not_cei_instances_tucker_5()
        res, _ = is_dichotomous_uniformly_euclidean(instance)
        self.assertTrue(not res)
