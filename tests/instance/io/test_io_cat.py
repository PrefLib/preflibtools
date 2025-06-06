import os
from unittest import TestCase

from preflibtools.instances import CategoricalInstance, get_parsed_instance
from tests.instance.io.write_file_test import (
    write_test_cat_file,
    cat_test_str,
    write_test_soi_file,
)


class TestCatInstance(TestCase):
    def test_read_from_file(self):
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

    def test_read_from_str(self):
        write_test_cat_file("testInstance.cat")
        instance1 = CategoricalInstance("testInstance.cat")
        instance2 = CategoricalInstance()
        instance2.parse_str(cat_test_str(), data_type="cat")
        assert instance1.preferences == instance2.preferences
        os.remove("testInstance.cat")

    def test_read_from_url(self):
        instance = CategoricalInstance()
        instance.parse_url(
            "https://raw.githubusercontent.com/PrefLib/PrefLib-Data/main/datasets/00037%20-%20aamas/00037-00000001.cat"
        )

    def test_read_autocorrect(self):
        str_to_correct = """# FILE NAME: 00026-00000001.cat
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
        # CATEGORY NAME 1: SameName
        # CATEGORY NAME 2: SameName
        # CATEGORY NAME 3: SameName
        # CATEGORY NAME 4: SameName
        # ALTERNATIVE NAME 1: Megret
        # ALTERNATIVE NAME 2: Lepage
        # ALTERNATIVE NAME 3: Gluckstein
        # ALTERNATIVE NAME 4: Bayrou
        # ALTERNATIVE NAME 5: Chirac
        # ALTERNATIVE NAME 6: LePen
        # ALTERNATIVE NAME 7: Taubira
        # ALTERNATIVE NAME 8: SameName
        # ALTERNATIVE NAME 9: SameName
        # ALTERNATIVE NAME 10: SameName
        # ALTERNATIVE NAME 11: SameName
        # ALTERNATIVE NAME 12: SameName
        # ALTERNATIVE NAME 13: SameName
        # ALTERNATIVE NAME 14: SameName
        # ALTERNATIVE NAME 15: SameName
        # ALTERNATIVE NAME 16: SameName
        13: 5, {1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}, {}, {}
        13: 5, {1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}, {}, {}
        10: 5, {1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}, {}, {}
        10: 5, {1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}, {}, {}
        9: 5, {1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}, {}, {}"""
        instance = CategoricalInstance()
        instance.parse_str(str_to_correct, data_type="cat", autocorrect=True)
        assert len(set(instance.alternatives_name.values())) == 16
        assert len(set(instance.categories_name.values())) == 4
        assert len(instance.preferences) == 1
        assert sum(instance.multiplicity.values()) == 55

    def test_get_parsed_instances(self):
        write_test_cat_file("testInstance.cat")
        instance1 = get_parsed_instance("testInstance.cat")
        instance2 = CategoricalInstance("testInstance.cat")
        assert instance1.preferences == instance2.preferences
        os.remove("testInstance.cat")

    def test_read_errors(self):
        write_test_soi_file("testInstance.soi")
        instance = CategoricalInstance()
        with self.assertRaises(TypeError):
            instance.parse_file("testInstance.soi")
        os.remove("testInstance.soi")

    def test_write_to_file(self):
        write_test_cat_file("testInstance.cat")
        instance = CategoricalInstance("testInstance.cat")
        instance.write("new_testInstance")
        with open("testInstance.cat", "r", encoding="utf-8") as init_file:
            init_file_content = init_file.read()
        os.remove("testInstance.cat")
        with open("new_testInstance.cat", "r", encoding="utf-8") as new_file:
            new_file_content = new_file.read()
        os.remove("new_testInstance.cat")
        assert init_file_content == new_file_content
