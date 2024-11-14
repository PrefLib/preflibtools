import random
from unittest import TestCase

from preflibtools.properties.subdomains.dichotomous.partition import is_2_part, is_part
from tests.properties.subdomains.dichotomous.utils import (
    initialise_categorical_instance,
)


def generate_part_instance(num_alternatives, num_votes, num_partitions=None):
    alternatives = list(range(num_alternatives))
    if num_partitions is None:
        num_partitions = random.randint(2, num_alternatives - 1)
    cuts = sorted(random.sample(range(1, num_alternatives - 1), k=num_partitions - 1))

    instance = initialise_categorical_instance(num_alternatives)

    num_votes = max(1, num_votes // num_partitions)
    for _ in range(num_votes):
        previous_cut = 0
        for cut in cuts:
            instance.preferences.append([tuple(alternatives[previous_cut:cut])])
            previous_cut = cut
    return instance


def generate_not_part_instance(num_alternatives, num_votes, num_partitions=None):
    instance = generate_part_instance(
        num_alternatives, num_votes - 1, num_partitions=num_partitions
    )
    instance.preferences.append([(0, num_alternatives - 1)])
    return instance


class TestDichotomousPartition(TestCase):
    def test_positive_2_part(self):
        for _ in range(30):
            num_alts = random.randint(5, 100)
            num_votes = random.randint(5, 100)
            instance = generate_part_instance(num_alts, num_votes, num_partitions=2)
            self.assertTrue(is_2_part(instance)[0])
            self.assertTrue(is_part(instance)[0])

    def test_negative_2_part(self):
        for _ in range(30):
            num_alts = random.randint(5, 100)
            num_votes = random.randint(5, 100)
            instance = generate_not_part_instance(num_alts, num_votes, num_partitions=2)
            self.assertFalse(is_2_part(instance)[0])
            self.assertFalse(is_part(instance)[0])

    def test_positive_part(self):
        for _ in range(30):
            num_alts = random.randint(5, 100)
            num_votes = random.randint(5, 100)
            instance = generate_part_instance(num_alts, num_votes)
            self.assertTrue(is_part(instance)[0])

    def test_negative_part(self):
        for _ in range(30):
            num_alts = random.randint(5, 100)
            num_votes = random.randint(5, 100)
            instance = generate_not_part_instance(num_alts, num_votes)
            self.assertFalse(is_part(instance)[0])
