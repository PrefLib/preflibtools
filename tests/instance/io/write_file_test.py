def cat_test_str():
    return """# FILE NAME: 00026-00000001.cat
# TITLE: GylesNonains
# DESCRIPTION: this is my description
# DATA TYPE: cat
# MODIFICATION TYPE: original
# RELATES TO: 
# RELATED FILES: 00026-00000001.toc
# PUBLICATION DATE: 2021-06-25
# MODIFICATION DATE: 2022-09-16
# NUMBER ALTERNATIVES: 16
# NUMBER VOTERS: 365
# NUMBER UNIQUE PREFERENCES: 216
# NUMBER CATEGORIES: 4
# CATEGORY NAME 1: Yes
# CATEGORY NAME 2: No
# CATEGORY NAME 3: No1
# CATEGORY NAME 4: No2
# ALTERNATIVE NAME 1: Megret
# ALTERNATIVE NAME 2: Lepage
# ALTERNATIVE NAME 3: Gluckstein
# ALTERNATIVE NAME 4: Bayrou
# ALTERNATIVE NAME 5: Chirac
# ALTERNATIVE NAME 6: LePen
# ALTERNATIVE NAME 7: Taubira
# ALTERNATIVE NAME 8: Saint-Josse
# ALTERNATIVE NAME 9: Mamere
# ALTERNATIVE NAME 10: Jospin
# ALTERNATIVE NAME 11: Boutin
# ALTERNATIVE NAME 12: Hue
# ALTERNATIVE NAME 13: Chevenement
# ALTERNATIVE NAME 14: Madelin
# ALTERNATIVE NAME 15: Laguiller
# ALTERNATIVE NAME 16: Besancenot
13: 6, {1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}, {}, {}
13: {}, {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}, {}, {}
10: {9, 10}, {1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 16}, {}, {}
10: {1, 6}, {2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}, {}, {}
9: 5, {1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}, {}, {}
8: {4, 5}, {1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}, {}, {}
8: 8, {1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16}, {}, {}
7: {5, 6}, {1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}, {}, {}
6: {5, 8}, {1, 2, 3, 4, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16}, {}, {}
6: {4, 5, 14}, {1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16}, {}, {}
6: {5, 14}, {1, 2, 3, 4, 6, 7, 8, 9}, 10, {11, 12, 13, 15, 16}
4: 14, {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}, 15, 16
"""


def write_test_cat_file(filepath):
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(cat_test_str())


def soi_test_str():
    return """# FILE NAME: 00002-00000001.soi
# TITLE: Debian 2002 Leader
# DESCRIPTION: 
# DATA TYPE: soi
# MODIFICATION TYPE: original
# RELATES TO: 
# RELATED FILES: 00002-00000001.toc
# PUBLICATION DATE: 2021-06-22
# MODIFICATION DATE: 2022-09-16
# NUMBER ALTERNATIVES: 4
# NUMBER VOTERS: 475
# NUMBER UNIQUE ORDERS: 41
# ALTERNATIVE NAME 1: Branden Robinson
# ALTERNATIVE NAME 2: Raphael Hertzog
# ALTERNATIVE NAME 3: Bdale Garbee
# ALTERNATIVE NAME 4: None Of The Above
60: 3, 1, 2, 4
50: 1, 3, 2, 4
40: 3, 1, 2
34: 3, 2, 1, 4
31: 3, 2, 4, 1
29: 2, 3, 1, 4
29: 1, 3, 2
24: 2, 1, 3, 4
22: 1, 2, 3, 4
20: 3, 2, 1
15: 1, 3, 4, 2
14: 2, 3, 1
11: 3, 1, 4, 2
9: 2, 3, 4, 1
9: 3
"""


def write_test_soi_file(filepath):
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(soi_test_str())


def toi_test_str():
    return """# FILE NAME: 00002-00000001.soi
# TITLE: Debian 2002 Leader
# DESCRIPTION: 
# DATA TYPE: toi
# MODIFICATION TYPE: original
# RELATES TO: 
# RELATED FILES: 00002-00000001.toc
# PUBLICATION DATE: 2021-06-22
# MODIFICATION DATE: 2022-09-16
# NUMBER ALTERNATIVES: 4
# NUMBER VOTERS: 475
# NUMBER UNIQUE ORDERS: 41
# ALTERNATIVE NAME 1: Branden Robinson
# ALTERNATIVE NAME 2: Raphael Hertzog
# ALTERNATIVE NAME 3: Bdale Garbee
# ALTERNATIVE NAME 4: None Of The Above
60: 3, 1, {2, 4}
50: 1, 3, 2, 4
40: 3, 1, 2
34: {3, 2, 1}, 4
31: {3, 2}, {4, 1}
29: 2, 3, 1, 4
29: 1, 3, 2
24: 2, 1, 3, 4
22: 1, 2, 3, 4
20: 3, 2, 1
15: 1, 3, 4, 2
14: 2, 3, 1
11: 3, 1, 4, 2
9: 2, 3, 4, 1
9: 3
"""


def write_test_toi_file(filepath):
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(toi_test_str())


def wmd_test_str():
    return """# FILE NAME: 00036-00000001.wmd
# TITLE: Kidney Matching - 16 with 0
# DESCRIPTION: 
# DATA TYPE: wmd
# MODIFICATION TYPE: synthetic
# RELATES TO: 
# RELATED FILES: 00036-00000001.dat
# PUBLICATION DATE: 2021-06-25
# MODIFICATION DATE: 2022-09-16
# NUMBER ALTERNATIVES: 16
# NUMBER EDGES: 59
# ALTERNATIVE NAME 1: Pair 1
# ALTERNATIVE NAME 2: Pair 2
# ALTERNATIVE NAME 3: Pair 3
# ALTERNATIVE NAME 4: Pair 4
# ALTERNATIVE NAME 5: Pair 5
# ALTERNATIVE NAME 6: Pair 6
# ALTERNATIVE NAME 7: Pair 7
# ALTERNATIVE NAME 8: Pair 8
# ALTERNATIVE NAME 9: Pair 9
# ALTERNATIVE NAME 10: Pair 10
# ALTERNATIVE NAME 11: Pair 11
# ALTERNATIVE NAME 12: Pair 12
# ALTERNATIVE NAME 13: Pair 13
# ALTERNATIVE NAME 14: Pair 14
# ALTERNATIVE NAME 15: Pair 15
# ALTERNATIVE NAME 16: Pair 16
1, 5, 1.0
1, 6, 1.0
2, 1, 1.0
2, 3, 1.0
2, 11, 1.0
2, 12, 1.0
3, 5, 1.0
3, 8, 1.0
4, 1, 1.0
4, 3, 1.0
4, 11, 1.0
6, 1, 1.0
6, 3, 1.0
6, 11, 1.0
7, 1, 1.0
7, 3, 1.0
7, 11, 1.0
7, 12, 1.0
8, 1, 1.0
8, 3, 1.0
8, 11, 1.0
9, 1, 1.0
9, 3, 1.0
9, 11, 1.0
9, 12, 1.0
10, 1, 1.0
10, 2, 1.0
10, 3, 1.0
10, 5, 1.0
10, 8, 1.0
10, 9, 1.0
10, 11, 1.0
10, 12, 1.0
10, 14, 1.0
10, 15, 1.0
10, 16, 1.0
12, 1, 1.0
12, 3, 1.0
12, 11, 1.0
13, 2, 1.0
13, 3, 1.0
13, 5, 1.0
13, 7, 1.0
13, 8, 1.0
13, 9, 1.0
13, 11, 1.0
13, 14, 1.0
13, 15, 1.0
13, 16, 1.0
14, 1, 1.0
14, 3, 1.0
14, 11, 1.0
14, 12, 1.0
15, 1, 1.0
15, 3, 1.0
15, 11, 1.0
16, 5, 1.0
16, 6, 1.0
16, 8, 1.0
"""


def write_test_wmd_file(filepath):
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(wmd_test_str())
