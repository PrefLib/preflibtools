import os

from preflibtools.instances import *


def write_test_soi_file(filepath):
    file = open(filepath, "w", encoding="utf-8")
    file.write(
        """# FILE NAME: 00002-00000001.soi
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
60: 3,1,2,4
50: 1,3,2,4
40: 3,1,2
34: 3,2,1,4
31: 3,2,4,1
29: 2,3,1,4
29: 1,3,2
24: 2,1,3,4
22: 1,2,3,4
20: 3,2,1
15: 1,3,4,2
14: 2,3,1
11: 3,1,4,2
9: 2,3,4,1
9: 3
""")
    file.close()


def write_test_cat_file(filepath):
    file = open(filepath, "w", encoding="utf-8")
    file.write("""# FILE NAME: 00026-00000001.cat
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
13: 6,{1,2,3,4,5,7,8,9,10,11,12,13,14,15,16},{},{}
13: {},{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16},{},{}
10: {9,10},{1,2,3,4,5,6,7,8,11,12,13,14,15,16},{},{}
10: {1,6},{2,3,4,5,7,8,9,10,11,12,13,14,15,16},{},{}
9: 5,{1,2,3,4,6,7,8,9,10,11,12,13,14,15,16},{},{}
8: {4,5},{1,2,3,6,7,8,9,10,11,12,13,14,15,16},{},{}
8: 8,{1,2,3,4,5,6,7,9,10,11,12,13,14,15,16},{},{}
7: {5,6},{1,2,3,4,7,8,9,10,11,12,13,14,15,16},{},{}
6: {5,8},{1,2,3,4,6,7,9,10,11,12,13,14,15,16},{},{}
6: {4,5,14},{1,2,3,6,7,8,9,10,11,12,13,15,16},{},{}
6: {5,14},{1,2,3,4,6,7,8,9},10,{11,12,13,15,16}
4: 14,{1,2,3,4,5,6,7,8,9,10,11,12,13},15,16
""")


def write_test_wmd_file(filepath):
    file = open(filepath, "w", encoding="utf-8")
    file.write(
        """# FILE NAME: 00036-00000001.wmd
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
1,5,1.0
1,6,1.0
2,1,1.0
2,3,1.0
2,11,1.0
2,12,1.0
3,5,1.0
3,8,1.0
4,1,1.0
4,3,1.0
4,11,1.0
6,1,1.0
6,3,1.0
6,11,1.0
7,1,1.0
7,3,1.0
7,11,1.0
7,12,1.0
8,1,1.0
8,3,1.0
8,11,1.0
9,1,1.0
9,3,1.0
9,11,1.0
9,12,1.0
10,1,1.0
10,2,1.0
10,3,1.0
10,5,1.0
10,8,1.0
10,9,1.0
10,11,1.0
10,12,1.0
10,14,1.0
10,15,1.0
10,16,1.0
12,1,1.0
12,3,1.0
12,11,1.0
13,2,1.0
13,3,1.0
13,5,1.0
13,7,1.0
13,8,1.0
13,9,1.0
13,11,1.0
13,14,1.0
13,15,1.0
13,16,1.0
14,1,1.0
14,3,1.0
14,11,1.0
14,12,1.0
15,1,1.0
15,3,1.0
15,11,1.0
16,5,1.0
16,6,1.0
16,8,1.0
""")
    file.close()


def test_read():
    write_test_soi_file("testInstance.soi")
    instance = OrdinalInstance("testInstance.soi")
    assert instance.file_path == "testInstance.soi"
    assert instance.file_name == "00002-00000001.soi"
    assert instance.data_type == "soi"
    assert instance.num_alternatives == 4
    assert instance.alternatives_name[1] == "Branden Robinson"
    assert instance.alternatives_name[2] == "Raphael Hertzog"
    assert instance.alternatives_name[4] == "None Of The Above"
    assert instance.num_voters == 475
    assert instance.num_unique_orders == 41
    order0 = ((3,), (1,), (2,), (4,))
    assert instance.orders[0] == order0
    assert instance.multiplicity[order0] == 60
    order6 = ((1,), (3,), (2,))
    assert instance.orders[6] == order6
    assert instance.multiplicity[order6] == 29
    os.remove("testInstance.soi")

    write_test_cat_file("testInstance.cat")
    instance = CategoricalInstance("testInstance.cat")
    assert instance.file_path == "testInstance.cat"
    assert instance.file_name == "00026-00000001.cat"
    assert instance.data_type == "cat"
    assert instance.description == "this is my description"
    assert instance.title == "GylesNonains"
    assert instance.modification_type == "original"
    assert instance.related_files == "00026-00000001.toc"
    assert instance.num_alternatives == 16
    assert instance.num_voters == 365
    assert instance.num_unique_preferences == 216
    assert instance.num_categories == 4
    assert instance.categories_name[1] == "Yes"
    assert instance.categories_name[2] == "No"
    assert instance.categories_name[3] == "No1"
    assert instance.categories_name[4] == "No2"
    assert instance.alternatives_name[1] == "Megret"
    assert instance.alternatives_name[8] == "Saint-Josse"
    assert instance.alternatives_name[10] == "Jospin"
    pref0 = ((6,), (1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16), (), ())
    assert instance.preferences[0] == pref0
    assert instance.multiplicity[pref0] == 13
    pref1 = ((5, 14), (1, 2, 3, 4, 6, 7, 8, 9), (10,), (11, 12, 13, 15, 16))
    assert instance.preferences[10] == pref1
    assert instance.multiplicity[pref1] == 6
    pref2 = ((14,), (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), (15,), (16,))
    assert instance.preferences[11] == pref2
    assert instance.multiplicity[pref2] == 4
    os.remove("testInstance.cat")


def test_write():
    write_test_soi_file("testInstance.soi")
    instance = OrdinalInstance("testInstance.soi")
    instance.write("testInstance_new.soi")
    init_file = open("testInstance.soi", "r", encoding="utf-8")
    init_file_content = init_file.read()
    init_file.close()
    new_file = open("testInstance_new.soi", "r", encoding="utf-8")
    new_file_content = new_file.read()
    new_file.close()
    assert init_file_content == new_file_content
    os.remove("testInstance.soi")
    os.remove("testInstance_new.soi")

    write_test_wmd_file("testInstance.wmd")
    instance = MatchingInstance("testInstance.wmd")
    instance.write("testInstance_new.wmd")
    init_file = open("testInstance.wmd", "r", encoding="utf-8")
    init_file_lines = init_file.readlines()
    init_file.close()
    new_file = open("testInstance_new.wmd", "r", encoding="utf-8")
    new_file_lines = new_file.readlines()
    new_file.close()
    assert len(init_file_lines) == len(new_file_lines)
    for line in init_file_lines:
        if line not in new_file_lines:
            assert False
    for line in new_file_lines:
        if line not in init_file_lines:
            assert False
    os.remove("testInstance.wmd")
    os.remove("testInstance_new.wmd")


def order_handling_test():
    instance = OrdinalInstance()
    orders = [((0,), (1,), (2,)), ((2,), (0,), (1,))]
    instance.append_order_list(orders)
    assert instance.num_alternatives == 3
    assert instance.data_type == "soc"
    assert instance.num_voters == 2
    assert instance.orders == orders
    assert instance.multiplicity[((0,), (1,), (2,))] == 1
    assert instance.multiplicity[((2,), (0,), (1,))] == 1
    assert instance.flatten_strict() == [((0, 1, 2), 1), ((2, 0, 1), 1)]
    orders += [((0,), (1, 2))]
    instance.append_order_list(orders)
    assert instance.num_alternatives == 3
    assert instance.data_type == "toc"
    assert instance.num_voters == 5
    assert instance.multiplicity[((0,), (1,), (2,))] == 2
    assert instance.multiplicity[((2,), (0,), (1,))] == 2
    assert instance.multiplicity[((0,), (1, 2))] == 1
    orders += [((4, 3), (1, 2))]
    instance.append_order_list(orders)
    assert instance.num_alternatives == 5
    assert instance.data_type == "toi"
    assert instance.num_voters == 9
    assert instance.multiplicity[((0,), (1,), (2,))] == 3
    assert instance.multiplicity[((2,), (0,), (1,))] == 3
    assert instance.multiplicity[((0,), (1, 2))] == 2
    assert instance.multiplicity[((4, 3), (1, 2))] == 1

    instance = OrdinalInstance()
    vote_map = {((0,), (1,), (2,)): 3, ((2,), (0,), (1,)): 2}
    instance.append_vote_map(vote_map)
    assert instance.num_alternatives == 3
    assert instance.data_type == "soc"
    assert instance.num_voters == 5
    assert len(instance.full_profile()) == 5
    assert instance.orders == [((0,), (1,), (2,)), ((2,), (0,), (1,))] or instance.orders == [((2,), (0,), (1,)),
                                                                                              ((0,), (1,), (2,))]
    vote_map = {((0,), (1,), (2,)): 3, ((2,), (0,), (1,)): 2, ((0,), (1, 2)): 4, ((4, 3), (1, 2)): 2}
    instance.append_vote_map(vote_map)
    assert instance.num_alternatives == 5
    assert instance.data_type == "toi"
    assert instance.num_voters == 16
    assert len(instance.full_profile()) == 16

    voteMapNew = instance.vote_map()
    assert voteMapNew[((0,), (1,), (2,))] == 6
    assert voteMapNew[((2,), (0,), (1,))] == 4
    assert voteMapNew[((0,), (1, 2))] == 4
    assert voteMapNew[((4, 3), (1, 2))] == 2


def test_populate():
    instance = OrdinalInstance()
    instance.populate_IC(5, 10)
    assert instance.num_voters == 5
    assert instance.num_alternatives == 10

    instance = OrdinalInstance()
    instance.populate_IC_anon(5, 10)
    assert instance.num_voters == 5
    assert instance.num_alternatives == 10

    instance = OrdinalInstance()
    instance.populate_urn(5, 10, 76)
    assert instance.num_voters == 5
    assert instance.num_alternatives == 10

    instance = OrdinalInstance()
    exception_raised = False
    try:
        instance.populate_urn(10, 30, 2)
    except ValueError:
        exception_raised = True
    assert exception_raised

    instance = OrdinalInstance()
    instance.populate_urn(30, 10, 2)
    assert instance.num_voters == 30
    assert instance.num_alternatives == 10

    instance = OrdinalInstance()
    instance.populate_urn(30, 2, 2)
    assert instance.num_voters == 30
    assert sum(instance.multiplicity.values()) == 30
    assert instance.num_alternatives == 2

    instance = OrdinalInstance()
    instance.populate_mallows(5, 3, [0.4, 0.6], [0.2, 0.3], [((0,), (1,), (2,)), ((1,), (0,), (2,))])
    assert instance.num_voters == 5
    assert instance.num_alternatives == 3

    instance = OrdinalInstance()
    instance.populate_mallows(5, 3, [10, 20], [0.2, 0.3], [((0,), (1,), (2,)), ((1,), (0,), (2,))])
    assert instance.num_voters == 5
    assert instance.num_alternatives == 3

    instance = OrdinalInstance()
    instance.populate_mallows_mix(5, 10, 5)
    assert instance.num_voters == 5
    assert instance.num_alternatives == 10

    exception_raised = False
    try:
        instance = OrdinalInstance()
        instance.populate_mallows(5, 3, [0.4, 0.6, 0.7], [0.2, 0.3], [((0,), (1,), (2,)), ((1,), (0,), (2,))])
    except ValueError:
        exception_raised = True
    assert exception_raised

    exception_raised = False
    try:
        instance = OrdinalInstance()
        instance.populate_mallows(5, 3, [0.4, 0.6], [0.2, 0.3, 0.4], [((0,), (1,), (2,)), ((1,), (0,), (2,))])
    except ValueError:
        exception_raised = True
    assert exception_raised

    exception_raised = False
    try:
        instance = OrdinalInstance()
        instance.populate_mallows(5, 3, [0.4, 0.6], [0.2, 0.3], [((0,), (1,), (2,)), ((1,), (0,), (2,)),
                                                                 ((0,), (2,), (1,))])
    except ValueError:
        exception_raised = True
    assert exception_raised


def main():
    print("Test write...")
    test_write()
    print("Test read...")
    test_read()
    print("Test handling of orders...")
    order_handling_test()
    print("Test populating instances...")
    test_populate()
    print("All tests successful")


if __name__ == "__main__":
    main()
