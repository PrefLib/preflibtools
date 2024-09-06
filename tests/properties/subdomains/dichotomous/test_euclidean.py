import random

from unittest import TestCase

from preflibtools.properties.subdomains.dichotomous.euclidean import is_dichotomous_euclidean
from tests.properties.subdomains.dichotomous.test_interval import generate_candidate_interval_instances, \
    generate_not_candidate_interval_instances, generate_not_candidate_interval_t1_instances, \
    generate_not_candidate_interval_t2_instances, generate_not_candidate_interval_t3_instances, \
    generate_not_candidate_interval_t4_instances, generate_not_candidate_interval_t5_instances


class TestDichotomousEuclidean(TestCase):
    def test_positive_ci(self):
        for _ in range(30):
            num_alternatives = random.randint(5, 20)
            num_voters = random.randint(5, 20)
            instance = generate_candidate_interval_instances(num_alternatives, num_voters)
            self.assertTrue(is_dichotomous_euclidean(instance)[0])

    def test_negative_ci(self):
        for _ in range(30):
            num_alternatives = random.randint(5, 20)
            num_voters = random.randint(5, 20)
            instance = generate_not_candidate_interval_instances(num_alternatives, num_voters)
            self.assertFalse(is_dichotomous_euclidean(instance)[0])

    def test_negative_ci_cei_t1(self):
        for _ in range(30):
            num_alternatives = random.randint(5, 20)
            instance = generate_not_candidate_interval_t1_instances(num_alternatives)
            self.assertFalse(is_dichotomous_euclidean(instance)[0])

    def test_negative_ci_cei_t2(self):
        for _ in range(30):
            num_alternatives = random.randint(5, 20)
            instance = generate_not_candidate_interval_t2_instances(num_alternatives)
            self.assertFalse(is_dichotomous_euclidean(instance)[0])

    def test_negative_ci_cei_t3(self):
        for _ in range(30):
            num_alternatives = random.randint(5, 20)
            instance = generate_not_candidate_interval_t3_instances(num_alternatives)
            self.assertFalse(is_dichotomous_euclidean(instance)[0])

    def test_negative_ci_cei_t4(self):
        instance = generate_not_candidate_interval_t4_instances()
        self.assertFalse(is_dichotomous_euclidean(instance)[0])

    def test_negative_ci_cei_t5(self):
        instance = generate_not_candidate_interval_t5_instances()
        self.assertFalse(is_dichotomous_euclidean(instance)[0])
