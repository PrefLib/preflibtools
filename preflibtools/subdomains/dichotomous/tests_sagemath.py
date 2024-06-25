from pq_trees import reorder_sets
import sys
from tqdm import tqdm, trange
import random
import json

def isC1P(matrix):
    # transpose matrix
    transposed_matrix = list(zip(*matrix))
    cols = list(range(len(transposed_matrix[0])))
    sets = []
    for row in transposed_matrix:
        sets.append([c for c in cols if row[c] == 1])
    try:
        reorder_sets(sets)
        return True
    except ValueError:
        return False
    raise ValueError("Should not reach here")

def shuffleColumns(matrix):
    perm = list(range(len(matrix[0])))
    random.shuffle(perm)
    new_matrix = []
    for row in matrix:
        new_matrix.append([row[i] for i in perm])
    return new_matrix

# Positive tests
print("Testing positive examples...")
for _ in trange(100):
    n = random.randint(5, 100)
    m = random.randint(5, 100)
    matrix = []
    for _ in range(m):
        left = random.randint(0, n - 2)
        right = random.randint(left + 1, n - 1)
        row = [1 if left <= i <= right else 0 for i in range(n)]
        matrix.append(row)
    for _ in range(10):
        assert isC1P(shuffleColumns(matrix))

# Negative tests
def tuckerI(k):
    xs = list(range(k+2))
    matrix = []
    for begin in range(k+1):
        row = [0] * (k+2)
        row[begin] = 1
        row[begin+1] = 1
        matrix.append(row)
    row = [0] * (k+2)
    row[0] = 1
    row[-1] = 1
    matrix.append(row)
    return matrix

def tuckerII(k):
    xs = list(range(k+3))
    matrix = []
    for begin in range(k+1):
        row = [0] * (k+3)
        row[begin] = 1
        row[begin+1] = 1
        matrix.append(row)
    row = [1] * (k+3)
    row[0] = 0
    matrix.append(row)
    row = [1] * (k+3)
    row[-2] = 0
    matrix.append(row)
    return matrix

def tuckerIII(k):
    xs = list(range(k+3))
    matrix = []
    for begin in range(k+1):
        row = [0] * (k+3)
        row[begin] = 1
        row[begin+1] = 1
        matrix.append(row)
    row = [1] * (k+3)
    row[0] = 0
    row[-2] = 0
    matrix.append(row)
    return matrix

tuckerIV = [
    [1,1,0,0,0,0],
    [0,0,1,1,0,0],
    [0,0,0,0,1,1],
    [1,0,1,0,1,0]
]

tuckerV = [
    [1,1,0,0,0],
    [0,0,1,1,0],
    [1,1,1,1,0],
    [1,0,1,0,1]
]

tucker_matrices = [tuckerIV, tuckerV]
for k in range(2, 10):
    tucker_matrices.append(tuckerI(k))
    tucker_matrices.append(tuckerII(k))
    tucker_matrices.append(tuckerIII(k))

print("Testing Tucker matrices...")
for matrix in tucker_matrices:
    if isC1P(matrix):
        for row in matrix:
            print("".join(str(x) for x in row))
    assert not isC1P(matrix)

print("Testing negative examples...")
for _ in trange(100):
    # blow up and shuffle Tucker matrices to obtain negative examples
    matrix = random.choice(tucker_matrices)
    n = len(matrix[0])
    # add some random rows
    for _ in range(random.randint(1, 10)):
        matrix.append([random.randint(0,1) for _ in range(n)])
    # add some random columns
    for _ in range(random.randint(1, 10)):
        for row in matrix:
            row.append(random.randint(0,1))
    for _ in range(10):
        # shuffle rows
        random.shuffle(matrix)
        assert not isC1P(shuffleColumns(matrix))