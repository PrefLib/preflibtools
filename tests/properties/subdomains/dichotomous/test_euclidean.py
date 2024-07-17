import unittest
import random
from prefsampling import EuclideanSpace
from prefsampling.approval import euclidean_vcr
from itertools import combinations


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
            res, _ = is_DUE(instance)
            self.assertTrue(res == True or res is None)

    def test_negative_examples_due_prefsampling_added_votes(self):
        for _ in trange(100):
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
            res, _ = is_DUE(instance)
            self.assertTrue(res == False or res is None)

    def test_positive_examples_due_wsc(self):
        for _ in trange(100):
            a = random.randint(10, 20)
            alternatives = [i for i in range(a)]
            v = random.randint(5, len(list(combinations(alternatives, 2))))
            instance = generate_WSC_instance(a, v)
            res, _ = is_DUE(instance)
            self.assertTrue(res == True or res is None)

    def test_negative_examples_due_wsc(self):
        for _ in trange(100):
            a = random.randint(10, 20)
            alternatives = [i for i in range(a)]
            v = random.randint(5, len(list(combinations(alternatives, 2))))
            instance = generate_NOT_WSC_instance(a, v)
            res, _ = is_DUE(instance)
            self.assertTrue(res == False or res is None)

    def test_positive_examples_due_cei(self):
        for _ in trange(1):
            a = random.randint(5, 100)
            v = random.randint(5, 100)
            instance = generate_CEI_instances(a, v)
            res, _ = is_DUE(instance)
            self.assertTrue(res == True)

    def test_positive_examples_due_vei(self):
        for _ in trange(1):
            a = random.randint(5, 100)
            v = random.randint(5, 100)
            instance = generate_VEI_instances(a, v)
            res, _ = is_DUE(instance)
            self.assertTrue(res == True)

    def test_positive_examples_due_part(self):
        for _ in trange(1):
            a = random.randint(5, 100)
            v = random.randint(5, 100)
            instance = generate_PART_instances(a, v)
            res, _ = is_DUE(instance)
            self.assertTrue(res == True)

    def test_negative_examples_due_not_ci(self):
        for _ in trange(10):
            a = random.randint(5, 30)
            v = random.randint(5, 100)
            instance = generate_NOT_CI_instances(a, v)
            res, _ = is_DUE(instance)
            self.assertTrue(res == False)

    def test_negative_examples_due_t1(self):
        for _ in trange(10):
            a = random.randint(5, 30)
            instance = generate_NOT_CI_CEI_instances_T1(a)
            res, _ = is_DUE(instance)
            self.assertTrue(res == False)

    def test_negative_examples_due_t2(self):
        for _ in trange(10):
            a = random.randint(5, 30)
            instance = generate_NOT_CI_CEI_instances_T2(a)
            res, _ = is_DUE(instance)
            self.assertTrue(res == False)

    def test_negative_examples_due_t3(self):
        for _ in trange(10):
            a = random.randint(5, 30)
            instance = generate_NOT_CI_CEI_instances_T3(a)
            res, _ = is_DUE(instance)
            self.assertTrue(res == False)

    def test_negative_examples_due_t4(self):
        for _ in trange(1):
            a = random.randint(5, 30)
            instance = instance_NOT_CI_CEI_T4
            res, _ = is_DUE(instance)
            self.assertTrue(res == False)

    def test_negative_examples_due_t5(self):
        for _ in trange(1):
            a = random.randint(5, 30)
            instance = instance_NOT_CI_CEI_T5
            res, _ = is_DUE(instance)
            self.assertTrue(res == False)


if __name__ == '__main__':
    unittest.main()
