import unittest
import random

from instances import CategoricalInstance
from properties.subdomains.dichotomous.interval import is_candidate_interval, \
    is_candidate_extremal_interval, is_voter_interval, is_voter_extremal_interval


def base_cat_instance(num_alt):
    instance = CategoricalInstance()
    instance.num_alternatives = num_alt
    instance.alternatives_name = {i: i for i in range(num_alt)}
    instance.num_categories = 1
    instance.categories_name = {0: "Approved"}
    return instance


def generate_ci_instances(num_alt, num_votes):
    instance = base_cat_instance(num_alt)
    for _ in range(num_votes):
        left_bound = random.randint(0, num_alt - 1)
        right_bound = random.randint(left_bound, num_alt)
        instance.preferences.append((tuple(range(left_bound, right_bound)),))
    return instance


def generate_not_ci_instances(num_alt, num_votes):
    instance = generate_ci_instances(num_alt, num_votes)
    for j in range(num_alt - 1):
        instance.preferences.append(((j,),))
        instance.preferences.append(((j, num_alt - 1),))
    return instance


def generate_cei_instances(num_alt, num_votes):
    instance = base_cat_instance(num_alt)
    for _ in range(num_votes):
        length = random.randint(0, num_alt - 1)
        if random.random() < 0.5:
            instance.preferences.append((tuple(range(0, length)),))
        else:
            instance.preferences.append((tuple(range(num_alt - length - 1, num_alt)),))
    return instance


def generate_not_cei_instances(num_alt, num_votes):
    instance = generate_cei_instances(num_alt, num_votes)
    for j in range(num_alt - 1):
        instance.preferences.append(((j,),))
        instance.preferences.append(((j, num_alt - 1),))
    return instance


def generate_not_cei_instances_tucker_1(num_alt):
    instance = base_cat_instance(num_alt)
    for i in range(num_alt - 1):
        instance.preferences.append(((i, i + 1),))
    instance.preferences.append(((0, num_alt - 1),))
    return instance


def generate_not_cei_instances_tucker_2(num_alt):
    instance = base_cat_instance(num_alt)
    for i in range(num_alt - 1):
        instance.preferences.append(((i, i + 1),))
    # Append all alternatives except the first one
    instance.preferences.append((tuple(range(1, num_alt)),))
    # Append all alternatives except the second to last
    instance.preferences.append((tuple(k for k in range(num_alt) if k != num_alt - 2),))
    return instance


def generate_not_cei_instances_tucker_3(num_alt):
    instance = base_cat_instance(num_alt)
    for i in range(num_alt - 1):
        instance.preferences.append(((i, i + 1),))
    # Append all alternatives except first and the second to last
    instance.preferences.append((tuple(k for k in range(1, num_alt) if k != num_alt - 2),))
    return instance


def generate_not_cei_instances_tucker_4():
    instance = base_cat_instance(6)
    instance.preferences.append(((0, 1),))
    instance.preferences.append(((2, 3),))
    instance.preferences.append(((4, 5),))
    instance.preferences.append(((1, 3, 5),))
    return instance


def generate_not_cei_instances_tucker_5():
    instance = base_cat_instance(5)
    instance.preferences.append(((0, 1),))
    instance.preferences.append(((0, 1, 2, 3),))
    instance.preferences.append(((2, 3),))
    instance.preferences.append(((0, 3, 4),))
    return instance


def generate_vi_instances(num_alt, num_votes):
    instance = base_cat_instance(num_alt)
    votes = [set() for _ in range(num_votes)]
    for alt in range(num_alt):
        left_bound = random.randint(0, num_votes - 1)
        right_bound = random.randint(left_bound, num_votes)
        for voter in range(left_bound, right_bound):
            votes[voter].add(alt)
    for vote in votes:
        instance.preferences.append((tuple(vote),))
    return instance


def generate_vei_instances(num_alt, num_votes):
    instance = base_cat_instance(num_alt)
    votes = [set() for _ in range(num_votes)]
    for alt in range(num_alt):
        length = random.randint(0, num_votes)
        if random.random() < 0.5:
            for voter in range(0, length):
                votes[voter].add(alt)
        else:
            for voter in range(num_votes - length, num_votes):
                votes[voter].add(alt)
    for vote in votes:
        instance.preferences.append((tuple(vote),))
    return instance


def generate_not_vi_instances_tucker_1(num_alt):
    instance = base_cat_instance(num_alt)
    votes = [set() for _ in range(num_alt)]

    # Add two alternatives around the diagonal to votes
    for i in range(num_alt - 1):
        votes[i].add(i)
        votes[i + 1].add(i)
    # Add last alternative to first vote
    votes[0].add(num_alt - 1)
    # Add last alternative to last vote
    votes[-1].add(num_alt - 1)

    for vote in votes:
        instance.preferences.append((tuple(vote),))
    return instance


def generate_not_vi_instances_tucker_2(num_alt):
    instance = base_cat_instance(num_alt)
    votes = [set() for _ in range(num_alt)]

    # Add two alternatives around the diagonal to votes
    for i in range(num_alt - 1):
        votes[i].add(i)
        votes[i + 1].add(i)

    # Add second to last alternative to all voters except first
    for i in range(1, num_alt):
        votes[i].add(num_alt - 2)

    # Add last alternative to all voters except second to last
    for i in range(num_alt - 2):
        votes[i].add(num_alt - 1)
    votes[-1].add(num_alt - 1)

    for vote in votes:
        instance.preferences.append((tuple(vote),))
    return instance


def generate_not_vi_instances_tucker_3(num_alt):
    instance = base_cat_instance(num_alt)
    votes = [set() for _ in range(num_alt)]

    # Add two alternatives around the diagonal to votes
    for i in range(num_alt - 1):
        votes[i].add(i)
        votes[i + 1].add(i)
    # Add second to last alternative to all voters except first
    for i in range(1, num_alt - 2):
        votes[i].add(num_alt - 1)

    # Add a vote with only last alternative
    votes.append({num_alt - 1})

    for vote in votes:
        instance.preferences.append((tuple(vote),))
    return instance


def generate_not_vi_instances_tucker_4():
    instance = base_cat_instance(4)
    instance.preferences.append(((0,),))
    instance.preferences.append(((0, 3),))
    instance.preferences.append(((1,),))
    instance.preferences.append(((1, 3),))
    instance.preferences.append(((2,),))
    instance.preferences.append(((2, 3),))
    return instance


def generate_not_vi_instances_tucker_5():
    instance = base_cat_instance(4)
    instance.preferences.append(((0, 1, 3),))
    instance.preferences.append(((0, 1),))
    instance.preferences.append(((1, 2),))
    instance.preferences.append(((1, 2, 3),))
    instance.preferences.append(((3,),))
    return instance


class TestInterval(unittest.TestCase):

    def test_is_ci(self):
        for _ in range(500):
            a = random.randint(5, 50)
            v = random.randint(5, 50)
            instance = generate_ci_instances(a, v)
            with self.subTest(instance=instance):
                res, ordering = is_candidate_interval(instance)
                self.assertTrue(res)
                self.assertEqual(len(set(ordering)), a)

    def test_is_not_ci(self):
        for _ in range(500):
            a = random.randint(5, 50)
            v = random.randint(5, 50)
            instance = generate_not_ci_instances(a, v)
            with self.subTest(instance=instance):
                res, _ = is_candidate_interval(instance)
                self.assertFalse(res)

        for _ in range(500):
            a = random.randint(5, 100)
            instance = generate_not_cei_instances_tucker_1(a)
            with self.subTest(instance=instance):
                res, _ = is_candidate_interval(instance)
                self.assertFalse(res)

        for _ in range(500):
            a = random.randint(5, 100)
            instance = generate_not_cei_instances_tucker_2(a)
            with self.subTest(instance=instance):
                res, _ = is_candidate_interval(instance)
                self.assertFalse(res)

        for _ in range(500):
            a = random.randint(5, 100)
            instance = generate_not_cei_instances_tucker_3(a)
            with self.subTest(instance=instance):
                res, _ = is_candidate_interval(instance)
                self.assertFalse(res)

        instance = generate_not_cei_instances_tucker_4()
        with self.subTest(instance=instance):
            res, _ = is_candidate_interval(instance)
            self.assertFalse(res)

        instance = generate_not_cei_instances_tucker_5()
        with self.subTest(instance=instance):
            res, _ = is_candidate_interval(instance)
            self.assertFalse(res)

    def test_is_cei(self):
        for _ in range(500):
            a = random.randint(5, 50)
            v = random.randint(5, 50)
            instance = generate_cei_instances(a, v)
            with self.subTest(instance=instance):
                res, _ = is_candidate_extremal_interval(instance)
                self.assertTrue(res)

    def test_is_not_cei(self):
        for _ in range(500):
            a = random.randint(5, 50)
            v = random.randint(5, 50)
            instance = generate_not_cei_instances(a, v)
            with self.subTest(instance=instance):
                res, _ = is_candidate_extremal_interval(instance)
                self.assertFalse(res)

        for _ in range(500):
            a = random.randint(5, 100)
            instance = generate_not_cei_instances_tucker_1(a)
            with self.subTest(instance=instance):
                res, _ = is_candidate_extremal_interval(instance)
                self.assertFalse(res)

        for _ in range(500):
            a = random.randint(5, 100)
            instance = generate_not_cei_instances_tucker_2(a)
            with self.subTest(instance=instance):
                res, _ = is_candidate_extremal_interval(instance)
                self.assertFalse(res)

        for _ in range(500):
            a = random.randint(5, 100)
            instance = generate_not_cei_instances_tucker_3(a)
            with self.subTest(instance=instance):
                res, _ = is_candidate_extremal_interval(instance)
                self.assertFalse(res)

        instance = generate_not_cei_instances_tucker_4()
        with self.subTest(instance=instance):
            res, _ = is_candidate_extremal_interval(instance)
            self.assertFalse(res)

        instance = generate_not_cei_instances_tucker_5()
        with self.subTest(instance=instance):
            res, _ = is_candidate_extremal_interval(instance)
            self.assertFalse(res)

    def test_is_vi(self):
        for _ in range(500):
            a = random.randint(5, 50)
            v = random.randint(5, 50)
            instance = generate_vi_instances(a, v)
            res, _ = is_voter_interval(instance)
            self.assertTrue(res)

    def test_is_not_vi(self):
        for _ in range(500):
            a = random.randint(5, 100)
            instance = generate_not_vi_instances_tucker_1(a)
            res, _ = is_voter_interval(instance)
            self.assertFalse(res)

        for _ in range(500):
            a = random.randint(5, 100)
            instance = generate_not_vi_instances_tucker_2(a)
            res, _ = is_voter_interval(instance)
            self.assertFalse(res)

        for _ in range(500):
            a = random.randint(5, 100)
            instance = generate_not_vi_instances_tucker_3(a)
            res, _ = is_voter_interval(instance)
            self.assertFalse(res)

        instance = generate_not_vi_instances_tucker_4()
        res, _ = is_voter_interval(instance)
        self.assertFalse(res)

        instance = generate_not_vi_instances_tucker_5()
        res, _ = is_voter_interval(instance)
        self.assertFalse(res)

    def text_is_vei(self):
        for _ in range(500):
            a = random.randint(5, 50)
            v = random.randint(5, 50)
            instance = generate_vei_instances(a, v)
            res, _ = is_voter_extremal_interval(instance)
            self.assertTrue(res)

    def text_is_not_vei(self):
        for _ in range(500):
            a = random.randint(5, 100)
            instance = generate_not_vi_instances_tucker_1(a)
            res, _ = is_voter_extremal_interval(instance)
            self.assertFalse(res)

        for _ in range(500):
            a = random.randint(5, 100)
            instance = generate_not_vi_instances_tucker_2(a)
            res, _ = is_voter_extremal_interval(instance)
            self.assertFalse(res)

        for _ in range(500):
            a = random.randint(5, 100)
            instance = generate_not_vi_instances_tucker_3(a)
            res, _ = is_voter_extremal_interval(instance)
            self.assertFalse(res)

        instance = generate_not_vi_instances_tucker_4()
        res, _ = is_voter_extremal_interval(instance)
        self.assertFalse(res)

        instance = generate_not_vi_instances_tucker_5()
        res, _ = is_voter_extremal_interval(instance)
        self.assertFalse(res)
