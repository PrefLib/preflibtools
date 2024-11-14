import random
from itertools import combinations
from unittest import TestCase

from preflibtools.properties.subdomains.dichotomous.singlecrossing import (
    is_weakly_single_crossing,
)
from tests.properties.subdomains.dichotomous.test_interval import (
    generate_not_candidate_interval_instances,
    generate_not_candidate_interval_t1_instances,
    generate_not_candidate_interval_t2_instances,
    generate_not_candidate_interval_t3_instances,
    generate_not_candidate_interval_t4_instances,
    generate_not_candidate_interval_t5_instances,
)
from tests.properties.subdomains.dichotomous.test_partition import (
    generate_part_instance,
)
from tests.properties.subdomains.dichotomous.utils import (
    initialise_categorical_instance,
)


def generate_weakly_single_crossing_instance(num_alternatives, num_voters):
    alternatives = list(range(num_alternatives))

    instance = initialise_categorical_instance(num_alternatives)

    group_size = max(1, num_voters // 3)

    instance.preferences = [[[]] for _ in range(group_size * 3)]
    v1 = range(group_size)
    v2 = range(group_size, len(instance.preferences) - group_size)
    v3 = range(len(instance.preferences) - group_size + 1, len(instance.preferences))

    for a, b in combinations(alternatives, 2):
        for v in v1:
            instance.preferences[v][0].append(a)
        for v in v2:
            instance.preferences[v][0].append(b)
        for v in v3:
            if random.random() < 0.5:
                instance.preferences[v][0].append(a)
                instance.preferences[v][0].append(b)
    return instance


class TestDichotomousWSC(TestCase):
    def test_positive_wsc(self):
        for _ in range(30):
            num_alternatives = random.randint(10, 20)
            num_voters = random.randint(10, 20)
            instance = generate_weakly_single_crossing_instance(
                num_alternatives, num_voters
            )
            self.assertTrue(is_weakly_single_crossing(instance)[0])

    def test_positive_wsc_2_part(self):
        for _ in range(30):
            num_alternatives = random.randint(10, 20)
            num_voters = random.randint(10, 20)
            instance = generate_part_instance(
                num_alternatives, num_voters, num_partitions=2
            )
            self.assertTrue(is_weakly_single_crossing(instance)[0])

    def test_negative_wsc_ci(self):
        for _ in range(30):
            num_alternatives = random.randint(10, 20)
            num_voters = random.randint(10, 20)
            instance = generate_not_candidate_interval_instances(
                num_alternatives, num_voters
            )
            self.assertFalse(is_weakly_single_crossing(instance)[0])
            instance = generate_not_candidate_interval_t1_instances(num_alternatives)
            self.assertFalse(is_weakly_single_crossing(instance)[0])
            instance = generate_not_candidate_interval_t2_instances(num_alternatives)
            self.assertFalse(is_weakly_single_crossing(instance)[0])
            instance = generate_not_candidate_interval_t3_instances(num_alternatives)
            self.assertFalse(is_weakly_single_crossing(instance)[0])
            instance = generate_not_candidate_interval_t4_instances()
            self.assertFalse(is_weakly_single_crossing(instance)[0])
            instance = generate_not_candidate_interval_t5_instances()
            self.assertFalse(is_weakly_single_crossing(instance)[0])
