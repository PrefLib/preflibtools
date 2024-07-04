from preflibtools.instances import OrdinalInstance
from preflibtools.properties.singlepeakedness import is_single_peaked
from prefsampling.ordinal import singlepeaked

import numpy as np
from itertools import combinations, product
from collections import defaultdict

def generate_k_axes_sp(num_voters_partition, num_alternatives, k, seed = None):
    """Generates a non-single-peaked profile by combining the votes of k profiles
    that are single-peaked on different axes.

    :param num_voters_partition: Number of orders in each partition.
    :type num_voters_1: int
    :param num_alternatives: Number of alternatives on which the orders are single-peaked.
    :type num_alternatives: int
    :param k: Number of single-peaked partitions the profile should contain.
    :type k: int
    :param seed: Seed for numpy random number generator
    :type seed: int

    :return: 
    :rtype: list(list)
    """
    rng = np.random.default_rng(seed)

    votes = singlepeaked.single_peaked_walsh(num_voters_partition, num_alternatives, seed=seed)
    axis_1 = tuple([i for i in range(num_alternatives)])

    axes_and_reverse = {axis_1: np.flip(np.array(axis_1))}

    alternative_mapping = np.array(axis_1)

    # Generate new axes
    for _ in range(k - 1):
        alternative_mapping = np.array(axis_1)

        axis_is_not_new = True
        while axis_is_not_new:
            rng.shuffle(alternative_mapping)

            for axis in axes_and_reverse:
                if ((axis != alternative_mapping).all()
                or (axes_and_reverse[axis] != alternative_mapping).all()):
                    axis_is_not_new = False
                    break
        
        axes_and_reverse[tuple(alternative_mapping)] = np.flip(alternative_mapping)

    # map votes to new axes
    for axis in axes_and_reverse:

        if axis != axis_1:
            for i in range(num_voters_partition):
                vote = np.array(axis_1)[votes[i]].tolist()

                votes.append(vote)
    
        votes.append(list(axis))
        votes.append(axes_and_reverse[axis].tolist())

    return votes

#########################################################################################

def two_axes_sp(instance):
    """Tests wether the collection of orders of the given instance can be split into
    two partitions such that each partition is itself a single-peaked instance. 
    In other words, whether the given instance is 2-axes single-peaked.
    This function implements an algorithm of Yang (2020).

    :param instance: the instance to test for 2-axes single-peakedness.
    :type instance: preflibtools.instances.preflibinstance.OrdinalInstance
    
    :return: whether the instance is 2-axes single-peaked, if that is the case,
    also provides the partitions as two lists of orders.
    :rtype: tuple(bool, list)
    """

    # Instance information
    unique_votes = [vote for vote, _ in instance.flatten_strict()]

    # Graph
    vertices = [None]
    edges = defaultdict(list)
    inv_edges = defaultdict(list)

    # Check if a WD exists
    has_wd = False
    wd_alternatives = None

    for votes in combinations(unique_votes, 3):
        
        has_wd, alts = is_WD(*votes)
        if has_wd:
            wd_alternatives = alts
            break
    
    if not has_wd:
        # If not, find all alpha sturctures
        for a, b in combinations(unique_votes, 2):
            if is_alpha(a, b): 
                add_clause((a, b), (1, 1), vertices, edges, inv_edges)
                add_clause((a, b), (-1, -1), vertices, edges, inv_edges)

    elif has_wd:
        # If exists, split votes based on last candidate of WD
        partitions = {alt: [] for alt in wd_alternatives}

        for vote in unique_votes:
            for alt in reversed(vote):
                if alt in wd_alternatives:
                    partitions[alt].append(vote)
                    break
        
        # Check if two of those splits are single-peaked
        valid_partitions = []
        invalid_partition = None

        for alt in partitions:
            instance = OrdinalInstance()
            instance.append_order_array(np.array(partitions[alt]))

            is_SP, _ = is_single_peaked(instance)

            if is_SP:
                valid_partitions.append(alt)
            else:
                invalid_partition = alt

        # Must have 2 single-peaked partitions
        if len(valid_partitions) < 2:
            return False, [None]
        elif len(valid_partitions) == 3:
            invalid_partition = valid_partitions.pop()
        
        # Find all WD and alpha in remaining partition
        a, b = valid_partitions[1], valid_partitions[0]
        c = invalid_partition

        other_partition = {
            a : b,
            b : a
        }

        clauses = {
            a : (-1, -1),
            b : (1, 1)
        }

        assigned_to = {
            a : defaultdict(lambda:False),
            b : defaultdict(lambda:False)
        }
        
        previous_vote = None
        for c_vote, c_vote_p in combinations(partitions[c], 2):

            for x in (a, b):
                y = other_partition[x]
                clause_vals = clauses[x]

                for x_vote in partitions[x]:

                    # Check WD between c, c' and x
                    is_wd, _ = is_WD(c_vote, c_vote_p, x_vote)
                    if is_wd:
                        add_clause((c_vote, c_vote_p), clause_vals, vertices, edges, inv_edges)
                    
                    if previous_vote != c_vote and not assigned_to[y][c_vote]:

                        # Check alpha between c, x
                        if is_alpha(c_vote, x_vote):
                            add_clause((c_vote, c_vote), clause_vals, vertices, edges, inv_edges)

                            # c can't be in partition x
                            assigned_to[y][c_vote] = True
                    
                    if previous_vote != c_vote and not assigned_to[y][c_vote]:
                        
                        # Check WD between c, x, and x'
                        for x_vote_p in partitions[x]:
                            if x_vote == x_vote_p:
                                continue

                            is_wd, _ = is_WD(c_vote, x_vote, x_vote_p)
                            if is_wd:
                                add_clause((c_vote, c_vote), clause_vals, vertices, edges, inv_edges)

                                # c can't be in partition x
                                assigned_to[y][c_vote] = True
                                break
                
                    # c can't be assigned to both partition x and y
                    if assigned_to[x][c_vote] and assigned_to[y][c_vote]:
                        return False, [None]
                    
            previous_vote = c_vote

    # Topologically ordered strongly connected components from kosaraju's alg
    solution = two_sat(vertices, edges, inv_edges)

    # Split the votes
    if not has_wd:
        votes_to_part = unique_votes
        final_partitions = [[], []]
    elif has_wd:
        votes_to_part = partitions[c]
        final_partitions = [partitions[b], partitions[a]]

    # Check the two_sat solution
    for vote in votes_to_part:
        # No restriction if not part of the cnf
        if vote not in vertices:
            final_partitions[0].append(vote)
        else:
            var = vertices.index(vote)

            # If p and not p are in same scc, np solution -> Vote can't be assigned to both partitions.
            if solution[var] == solution[-var]:
                return False, [None]
            
            # Assign true to literals in reverse topological ordering of scc.
            if solution[var] > solution[-var]:
                truth_value = 1
            else:
                truth_value = 0
            
            final_partitions[truth_value].append(vote)

    return True, final_partitions


def is_WD(v0, v1, v2):
    """A helper function for the 2-axes single-peaked function. Checks
    whether three votes contain a WD-structure.

    :param v0: order of alternatives.
    :type v0:

    :return: whether the three votes contain a WD-structure, if yes, also
    provides the involved alternatives.
    :rtype: tuple(bool, tuple)
    """

    # Find a
    a_candidates = v0[2:]
    for a in reversed(a_candidates):
        id_a0, id_a1 = v0.index(a), v1.index(a)

        must_have_bc = v0[:id_a0]
        b_candidates = v1[id_a1 + 1:]
        for b in reversed(b_candidates):
            if b not in must_have_bc:
                continue

            id_b1, id_b2, = v1.index(b), v2.index(b)

            must_have_c = v1[:id_b1]

            c_candidates = v2[id_b2 + 1:]
            for c in reversed(c_candidates):
                if (c not in must_have_c
                    or c not in must_have_bc):
                    continue

                id_c2 = v2.index(c)
                must_have_a = v2[:id_c2]

                if (a in must_have_a):
                    return True, (a, b, c)

    return False, (None,)


def is_alpha(v0, v1):
    """A helper function for the 2-axes single-peaked function.
    Tests whether two votes contain an alpha-structure.

    :param v0: Order of alternatives.
    :type v0: tuple

    :return: whether the two votes contain an alpha-structure
    :rtype: bool
    """
    if len(v0) < 4:
        return False
    
    # Find b candidates
    b_0 = v0[2:-1]
    b_1 = v1[2:-1]
    b_candidates = [b for b in b_0 if b in b_1]

    if len(b_candidates) == 0:
        return False
    
    # Find a and c candidates
    for b in b_candidates:
        id_b_0 = v0.index(b)
        id_b_1 = v1.index(b)

        a_0, c_0 = v0[:id_b_0], v0[id_b_0 + 1:]
        a_1, c_1 = v1[:id_b_1], v1[id_b_1 + 1:]

        a_candidates = [a for a in a_0 if a in c_1]
        c_candidates = [c for c in c_0 if c in a_1]

        # Check if d exists
        for a_c in product(a_candidates, c_candidates):
            d_0 = [d for d in a_0 if d in a_1 and (d not in a_c)]

            if len(d_0) != 0:
                return True
            
    return False


def add_clause(votes, clause, vertices, edges, inv_edges):
    """A helper function of the 2-axes single-peaked function.
    Adds the given votes to the list of vertices and creates new edges
    for the implication graph and its inverse according to the provided
    disjunctive clause.

    :param votes: Two orders of alternatives, being the propositions of the disjunction.
    :type votes: list(tuple)
    :param clause: Two values which are either 1 or -1 according to
    whether the propositions of the disjunction should be negated or not.
    :type clause: tuple(int)
    :param vertices: The implication graph's vertices.
    :type vertices: list
    :param edges: Edges of the implication graph.
    :type edges: dict
    :param inv_edges: Inverse of implication graph.
    :type inv_edges: dict
    """
    vote_1, vote_2 = votes
    val_1, val_2 = clause

    for vote in votes:
        if vote not in vertices:
            vertices.append(vote)
    
    # multiply by 1 or -1 based on whether the proposition should be negated.
    x = val_1 * vertices.index(vote_1)
    y = val_2 * vertices.index(vote_2)

    # (x v y) = (not x -> y)
    if y not in edges[-x]:
        edges[-x].append(y)
        inv_edges[y].append(-x)
    
    if x not in edges[-y]:
        edges[-y].append(x)
        inv_edges[x].append(-y)

#########################################################################################

def two_sat(vertices, edges, inv_edges):
    """A helper function for the k-alternative deletion algorithm.
    Implements Kosaraju's algorithm to find the strongly connected
    components of the given graph. Topologically orders the strongly
    connected components and finds which vertices belong to which component. 


    :return: dictionary pairing vertices with the topologically oredered
    strongly connected component it belongs to.
    :rtype: dict()
    """
    variables = [-i for i, _ in enumerate(reversed(vertices)) if i != 0] + [i for i, _ in enumerate(vertices) if i != 0]
    visited = {key: False for key in variables}
    assigned_scc = {key: None for key in variables}
    scc = defaultdict(set)
    L = []

    for u in variables:
        visit(u, visited, edges, L)

    for i, u in enumerate(reversed(L)):
        assign(u, i, inv_edges, scc, assigned_scc)

    return assigned_scc

def visit(u, visited, edges, L):
    if visited[u]:
        return
    
    visited[u] = True

    for v in edges[u]:
        visit(v, visited, edges, L)
    
    L.append(u)

def assign(u, root, edges, scc, assigned_scc):
    if assigned_scc[u] is not None:
        return
    
    assigned_scc[u] = root
    scc[root].add(u)

    for v in edges[u]:
        assign(v, root, edges, scc, assigned_scc)