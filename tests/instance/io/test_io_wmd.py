import os
from unittest import TestCase

from preflibtools.instances import MatchingInstance, get_parsed_instance
from tests.instance.io.write_file_test import write_test_wmd_file, write_test_cat_file, write_test_soi_file


class TestWmdInstances(TestCase):

    def test_get_parsed_instances(self):
        write_test_wmd_file("testInstance.wmd")
        instance1 = get_parsed_instance("testInstance.wmd")
        instance2 = MatchingInstance("testInstance.wmd")
        assert instance1.node_mapping == instance2.node_mapping
        os.remove("testInstance.wmd")

    def test_read_errors(self):
        write_test_soi_file("testInstance.soi")
        instance = MatchingInstance()
        with self.assertRaises(TypeError):
            instance.parse_file("testInstance.soi")
        os.remove("testInstance.soi")

        write_test_cat_file("testInstance.cat")
        instance = MatchingInstance()
        with self.assertRaises(TypeError):
            instance.parse_file("testInstance.cat")
        os.remove("testInstance.cat")

    def test_read_old(self):
        wmd_old_str = """16,27
        1,Pair 1 
        2,Pair 2 
        3,Pair 3 
        4,Pair 4 
        5,Pair 5 
        6,Pair 6 
        7,Pair 7 
        8,Pair 8 
        9,Pair 9 
        10,Pair 10 
        11,Pair 11 
        12,Pair 12 
        13,Pair 15 
        14,Pair 15 
        15,Pair 15 
        16,Pair 15
        0,4,1
        0,5,1
        1,11,1
        1,10,1
        1,0,1
        1,2,1
        2,4,1
        2,7,1
        3,10,1
        3,2,1
        3,0,1
        5,10,1
        5,0,1
        5,2,1
        6,0,1
        6,2,1
        6,11,1
        6,10,1
        7,2,1
        7,0,1
        7,10,1
        8,11,1
        8,12,1
        8,13,1
        8,14,1
        9,15,1
        9,15,1
        9,15,1
        9,15,1
        9,15,1
        9,15,1
        9,15,1
        9,15,1"""
        instance = MatchingInstance()
        instance.parse_old(wmd_old_str.split("\n"), autocorrect=True)
        assert len(set(instance.alternatives_name.values())) == 16
        assert instance.num_edges == 26
        assert len(instance.node_mapping) == 16

    def test_write_to_file(self):
        write_test_wmd_file("testInstance.wmd")
        instance = MatchingInstance("testInstance.wmd")
        instance.write("testInstance_new")
        with open("testInstance.wmd", "r", encoding="utf-8") as init_file:
            init_file_lines = init_file.readlines()
        os.remove("testInstance.wmd")
        with open("testInstance_new.wmd", "r", encoding="utf-8") as new_file:
            new_file_lines = new_file.readlines()
        os.remove("testInstance_new.wmd")
        assert len(init_file_lines) == len(new_file_lines)
        for line in init_file_lines:
            if line not in new_file_lines:
                assert False
        for line in new_file_lines:
            if line not in init_file_lines:
                assert False
