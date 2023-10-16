"""This module contains multiwinner voting rules."""

from preflibtools.aggregation.utilities import *
from preflibtools.properties.basic import *
from itertools import combinations


@requires_approval
def approval_chamberlin_courant_committee(instance, committeesize):
    candidates = instance.alternatives_name
    best_score = 0
    best_committees = list()
    for committee in combinations(candidates, committeesize):
        current_score = 0
        for order in instance.orders:
            multiplicity = instance.multiplicity[order]
            for a in order[0]:
                if a in committee:
                    current_score += multiplicity
        if current_score == best_score:
            best_committees.append(set(committee))
        elif current_score > best_score:
            best_committees = [set(committee), ]
            best_score = current_score
    return best_committees


@requires_preference_type("soc")
def borda_chamberlin_courant_committee(instance, committeesize):
    candidates = instance.alternatives_name
    best_score = 0
    best_committees = list()
    for committee in combinations(candidates, committeesize):
        current_score = 0
        for order in instance.orders:
            multiplicity = instance.multiplicity[order]
            for i in range(len(candidates)):
                if order[i][0] in committee:
                    current_score += multiplicity * (len(candidates) - i - 1)
                    break
        if current_score == best_score:
            best_committees.append(set(committee))
        elif current_score > best_score:
            best_committees = [set(committee), ]
            best_score = current_score
    return best_committees