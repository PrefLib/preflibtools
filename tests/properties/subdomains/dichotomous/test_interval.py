import random
from unittest import TestCase

from preflibtools.properties.subdomains.dichotomous.interval import (
    is_candidate_interval,
    is_candidate_extremal_interval,
    is_voter_interval,
    is_voter_extremal_interval,
)
from tests.properties.subdomains.dichotomous.utils import (
    initialise_categorical_instance,
)


def generate_candidate_interval_instances(num_alternatives, num_voters):
    alternatives = list(range(num_alternatives))
    instance = initialise_categorical_instance(num_alternatives)
    for _ in range(num_voters):
        left = random.randint(0, num_alternatives - 1)
        right = random.randint(left, num_alternatives)
        instance.preferences.append((tuple(alternatives[left:right]),))
    instance.factorise_instance(reset_multiplicity=True)
    instance.recompute_cardinality_param()
    return instance


def generate_not_candidate_interval_instances(num_alternatives, num_voters):
    instance = generate_candidate_interval_instances(num_alternatives, num_voters)
    alternatives = list(range(num_alternatives))
    for j in range(num_alternatives - 1):
        instance.preferences.append(((alternatives[j],),))
        instance.preferences.append(((alternatives[j], alternatives[-1]),))
    instance.factorise_instance(reset_multiplicity=True)
    instance.recompute_cardinality_param()
    return instance


def generate_candidate_extremal_interval_instances(num_alternatives, num_voters):
    alternatives = list(range(num_alternatives))
    instance = initialise_categorical_instance(num_alternatives)
    for _ in range(num_voters):
        cut = random.randint(1, num_alternatives - 1)
        if random.random():
            instance.preferences.append((tuple(alternatives[0:cut]),))
        else:
            instance.preferences.append((tuple(alternatives[cut:-1]),))
    instance.factorise_instance(reset_multiplicity=True)
    instance.recompute_cardinality_param()
    return instance


def generate_not_candidate_extremal_interval_instances(num_alternatives, num_voters):
    instance = generate_candidate_extremal_interval_instances(
        num_alternatives, num_voters
    )
    alternatives = list(range(num_alternatives))
    for j in range(num_alternatives - 1):
        instance.preferences.append(((alternatives[j],),))
        instance.preferences.append(((alternatives[j], alternatives[-1]),))
    instance.factorise_instance(reset_multiplicity=True)
    instance.recompute_cardinality_param()
    return instance


def generate_not_candidate_interval_t1_instances(num_alternatives):
    alternatives = list(range(num_alternatives))
    instance = initialise_categorical_instance(num_alternatives)
    # Add two alternatives around the diagonal as votes
    for j in range(num_alternatives - 1):
        instance.preferences.append(((alternatives[j], alternatives[j + 1]),))
    # Add vote on first and last alternative
    instance.preferences.append(((alternatives[0], alternatives[-1]),))
    instance.factorise_instance(reset_multiplicity=True)
    instance.recompute_cardinality_param()
    return instance


def generate_not_candidate_interval_t2_instances(num_alternatives):
    alternatives = list(range(num_alternatives))
    instance = initialise_categorical_instance(num_alternatives)
    # Add two alternatives around the diagonal as votes
    for j in range(num_alternatives - 1):
        instance.preferences.append(((alternatives[j], alternatives[j + 1]),))
    # Append all alternatives except the first one
    instance.preferences.append((tuple(alternatives[1:]),))
    # Append all alternatives except the second to last
    instance.preferences.append((tuple(alternatives[:-2] + alternatives[-1:]),))
    instance.factorise_instance(reset_multiplicity=True)
    instance.recompute_cardinality_param()
    return instance


def generate_not_candidate_interval_t3_instances(num_alternatives):
    alternatives = list(range(num_alternatives))
    instance = initialise_categorical_instance(num_alternatives)
    # Add two alternatives around the diagonal as votes
    for j in range(num_alternatives - 2):
        instance.preferences.append(((alternatives[j], alternatives[j + 1]),))
    # Append all alternatives except first and the second to last
    instance.preferences.append((tuple(alternatives[1:-2] + alternatives[-1:]),))
    instance.factorise_instance(reset_multiplicity=True)
    instance.recompute_cardinality_param()
    return instance


def generate_not_candidate_interval_t4_instances():
    instance = initialise_categorical_instance(6)
    instance.preferences.append(((0, 1),))
    instance.preferences.append(((2, 3),))
    instance.preferences.append(((4, 5),))
    instance.preferences.append(((0, 2, 4),))
    instance.factorise_instance(reset_multiplicity=True)
    instance.recompute_cardinality_param()
    return instance


def generate_not_candidate_interval_t5_instances():
    instance = initialise_categorical_instance(5)
    instance.preferences.append(((0, 1),))
    instance.preferences.append(((0, 1, 2, 3),))
    instance.preferences.append(((2, 3),))
    instance.preferences.append(((0, 3, 4),))
    instance.factorise_instance(reset_multiplicity=True)
    instance.recompute_cardinality_param()
    return instance


def generate_voter_interval_instances(num_alternatives, num_voters):
    alternatives = list(range(num_alternatives))
    instance = initialise_categorical_instance(num_alternatives)
    ballots = [[] for _ in range(num_voters)]
    for alt in alternatives:
        left = random.randint(0, num_voters - 1)
        right = random.randint(left, num_voters)
        for v in range(left, right):
            ballots[v].append(alt)
    instance.preferences = [(tuple(b),) for b in ballots]
    instance.factorise_instance(reset_multiplicity=True)
    instance.recompute_cardinality_param()
    return instance


def generate_voter_extremal_interval_instances(num_alternatives, num_voters):
    alternatives = list(range(num_alternatives))
    instance = initialise_categorical_instance(num_alternatives)
    ballots = [[] for _ in range(num_voters)]
    for alt in alternatives:
        cut = random.randint(1, num_voters - 1)
        if random.random() < 0.5:
            for v in range(cut):
                ballots[v].append(alt)
        else:
            for v in range(cut, num_voters):
                ballots[v].append(alt)
    instance.preferences = [(tuple(b),) for b in ballots]
    instance.factorise_instance(reset_multiplicity=True)
    instance.recompute_cardinality_param()
    return instance


def generate_not_voter_interval_t2_instances(num_voters):
    alternatives = list(range(num_voters + 1))
    instance = initialise_categorical_instance(num_voters + 1)
    ballots = [set() for _ in range(num_voters)]
    for v in range(num_voters - 1):
        ballots[v].add(alternatives[v])
        ballots[v].add(alternatives[v + 1])
        ballots[v].add(alternatives[-2])
        if v != num_voters - 3:
            ballots[v].add(alternatives[-1])
    ballots[-1].add(alternatives[0])
    ballots[-1].add(alternatives[-1])
    instance.preferences = [(tuple(b),) for b in ballots]
    instance.factorise_instance(reset_multiplicity=True)
    instance.recompute_cardinality_param()
    return instance


def generate_not_voter_interval_t3_instances(num_voters):
    alternatives = list(range(num_voters))
    instance = initialise_categorical_instance(num_voters)
    ballots = [set() for _ in range(num_voters)]
    for v in range(num_voters - 1):
        ballots[v].add(alternatives[v])
        ballots[v].add(alternatives[v + 1])
        if v != num_voters - 3:
            ballots[v].add(alternatives[-1])
    ballots[-1].add(alternatives[0])
    instance.preferences = [(tuple(b),) for b in ballots]
    instance.factorise_instance(reset_multiplicity=True)
    instance.recompute_cardinality_param()
    return instance


def generate_not_voter_interval_t4_instances():
    instance = initialise_categorical_instance(4)
    instance.preferences.append(((0, 3),))
    instance.preferences.append(((0,),))
    instance.preferences.append(((1, 3),))
    instance.preferences.append(((1,),))
    instance.preferences.append(((2, 3),))
    instance.preferences.append(((2,),))
    instance.factorise_instance(reset_multiplicity=True)
    instance.recompute_cardinality_param()
    return instance


def generate_not_voter_interval_t5_instances():
    instance = initialise_categorical_instance(4)
    instance.preferences.append(((0, 1, 3),))
    instance.preferences.append(((0, 1),))
    instance.preferences.append(((1, 2),))
    instance.preferences.append(((1, 2, 3),))
    instance.preferences.append(((3,),))
    instance.factorise_instance(reset_multiplicity=True)
    instance.recompute_cardinality_param()
    return instance


class TestDichotomousInterval(TestCase):
    def test_positive_ci(self):
        for _ in range(30):
            num_alternatives = random.randint(5, 20)
            num_voters = random.randint(5, 20)
            instance = generate_candidate_interval_instances(
                num_alternatives, num_voters
            )
            self.assertTrue(is_candidate_interval(instance)[0])

    def test_negative_ci(self):
        for _ in range(30):
            num_alternatives = random.randint(5, 20)
            num_voters = random.randint(5, 20)
            instance = generate_not_candidate_interval_instances(
                num_alternatives, num_voters
            )
            self.assertFalse(is_candidate_interval(instance)[0])
            self.assertFalse(is_candidate_extremal_interval(instance)[0])

    def test_negative_ci_cei_t1(self):
        for _ in range(30):
            num_alternatives = random.randint(5, 20)
            instance = generate_not_candidate_interval_t1_instances(num_alternatives)
            self.assertFalse(is_candidate_interval(instance)[0])
            self.assertFalse(is_candidate_extremal_interval(instance)[0])

    def test_negative_ci_cei_t2(self):
        for _ in range(30):
            num_alternatives = random.randint(5, 20)
            instance = generate_not_candidate_interval_t2_instances(num_alternatives)
            self.assertFalse(is_candidate_interval(instance)[0])
            self.assertFalse(is_candidate_extremal_interval(instance)[0])

    def test_negative_ci_cei_t3(self):
        for _ in range(30):
            num_alternatives = random.randint(5, 20)
            instance = generate_not_candidate_interval_t3_instances(num_alternatives)
            self.assertFalse(is_candidate_interval(instance)[0])
            self.assertFalse(is_candidate_extremal_interval(instance)[0])

    def test_negative_ci_cei_t4(self):
        instance = generate_not_candidate_interval_t4_instances()
        self.assertFalse(is_candidate_interval(instance)[0])
        self.assertFalse(is_candidate_extremal_interval(instance)[0])

    def test_negative_ci_cei_t5(self):
        instance = generate_not_candidate_interval_t5_instances()
        self.assertFalse(is_candidate_interval(instance)[0])
        self.assertFalse(is_candidate_extremal_interval(instance)[0])

    def test_positive_cei(self):
        for _ in range(30):
            num_alternatives = random.randint(5, 20)
            num_voters = random.randint(5, 20)
            instance = generate_candidate_extremal_interval_instances(
                num_alternatives, num_voters
            )
            self.assertTrue(is_candidate_extremal_interval(instance)[0])
            self.assertTrue(is_candidate_interval(instance)[0])

    def test_negative_cei(self):
        for _ in range(30):
            num_alternatives = random.randint(5, 20)
            num_voters = random.randint(5, 20)
            instance = generate_not_candidate_extremal_interval_instances(
                num_alternatives, num_voters
            )
            self.assertFalse(is_candidate_extremal_interval(instance)[0])

    def test_positive_vi(self):
        for _ in range(30):
            num_alternatives = random.randint(5, 100)
            num_voters = random.randint(5, 100)
            instance = generate_voter_interval_instances(num_alternatives, num_voters)
            self.assertTrue(is_voter_interval(instance)[0])

    def test_negative_vi_t1(self):
        for _ in range(30):
            num_alternatives = random.randint(5, 20)
            # The transposed matrix is generated by the same set of ballots as in CI
            instance = generate_not_candidate_interval_t1_instances(num_alternatives)
            self.assertFalse(is_voter_interval(instance)[0])
            self.assertFalse(is_voter_extremal_interval(instance)[0])

    def test_negative_vi_t2(self):
        for _ in range(30):
            num_voters = random.randint(5, 20)
            instance = generate_not_voter_interval_t2_instances(num_voters)
            self.assertFalse(is_voter_interval(instance)[0])
            self.assertFalse(is_voter_extremal_interval(instance)[0])

    def test_negative_vi_t3(self):
        for _ in range(30):
            num_voters = random.randint(5, 20)
            instance = generate_not_voter_interval_t3_instances(num_voters)
            self.assertFalse(is_voter_interval(instance)[0])
            self.assertFalse(is_voter_extremal_interval(instance)[0])

    def test_negative_vi_t4(self):
        instance = generate_not_voter_interval_t4_instances()
        self.assertFalse(is_voter_interval(instance)[0])
        self.assertFalse(is_voter_extremal_interval(instance)[0])

    def test_negative_vi_t5(self):
        instance = generate_not_voter_interval_t5_instances()
        self.assertFalse(is_voter_interval(instance)[0])
        self.assertFalse(is_voter_extremal_interval(instance)[0])

    def test_positive_vei(self):
        for _ in range(30):
            num_alternatives = random.randint(5, 100)
            num_voters = random.randint(5, 100)
            instance = generate_voter_extremal_interval_instances(
                num_alternatives, num_voters
            )
            self.assertTrue(is_voter_extremal_interval(instance)[0])
            self.assertTrue(is_voter_interval(instance)[0])
