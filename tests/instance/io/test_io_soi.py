import os
from unittest import TestCase

from preflibtools.instances import OrdinalInstance, get_parsed_instance
from tests.instance.io.write_file_test import write_test_soi_file, soi_test_str, write_test_cat_file


class TestSoiInstances(TestCase):

    def test_read_from_file(self):
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

    def test_read_from_str(self):
        write_test_soi_file("testInstance.soi")
        instance1 = OrdinalInstance("testInstance.soi")
        instance2 = OrdinalInstance()
        instance2.parse_str(soi_test_str(), data_type="soi")
        assert instance1.orders == instance2.orders
        os.remove("testInstance.soi")

    def test_read_from_url(self):
        instance = OrdinalInstance()
        instance.parse_url("https://www.preflib.org/static/data/apa/00028-00000007.soi")

    def test_autocorrect(self):
        instance = OrdinalInstance()
        instance.parse_str("""# FILE NAME: 00002-00000001.soi
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
        # ALTERNATIVE NAME 1: SameName
        # ALTERNATIVE NAME 2: SameName
        # ALTERNATIVE NAME 3: SameName
        # ALTERNATIVE NAME 4: SameName
        60: 3, 1, 2, 4
        50: 1, 3, 2, 4
        40: 3, 2, 4, 1
        34: 3, 2, 4, 1
        31: 3, 2, 4, 1""", data_type="soi", autocorrect=True)
        assert len(set(instance.alternatives_name.values())) == 4
        assert instance.multiplicity[((3,), (2,), (4,), (1,))] == 105

    def test_old_soi(self):
        old_soi_str = """12
        1,Cathal Boland F.G. 
        2,Clare Daly S.P. 
        3,Mick Davis S.F. 
        4,Jim Glennon F.F. 
        5,Ciaran Goulding Non-P 
        6,Michael Kennedy F.F. 
        7,Nora Owen F.G. 
        8,Eamonn Quinn Non-P 
        9,Sean Ryan Lab 
        10,SameName 
        11,SameName
        12,SameName
        43942,43942,19299
        800,12,6,4
        680,4,6,12
        506,6,12,4
        486,12,4,6
        429,6,4,12
        367,4,12,6
        343,10
        278,2
        251,9
        194,9"""
        instance = OrdinalInstance()
        instance.parse_old(old_soi_str.split("\n"), autocorrect=True)
        assert len(set(instance.alternatives_name.values())) == 12
        assert instance.multiplicity[((9,),)] == 445
        assert instance.orders[0] == ((12,), (6,), (4,))
        assert instance.orders[1] == ((4,), (6,), (12,))
        assert instance.orders[6] == ((10,),)

    def test_get_parsed_instances(self):
        write_test_soi_file("testInstance.soi")
        instance1 = get_parsed_instance("testInstance.soi")
        instance2 = OrdinalInstance("testInstance.soi")
        assert instance1.orders == instance2.orders
        os.remove("testInstance.soi")

    def test_read_errors(self):
        write_test_cat_file("testInstance.cat")
        instance = OrdinalInstance()
        with self.assertRaises(TypeError):
            instance.parse_file("testInstance.cat")
        os.remove("testInstance.cat")

    def test_write_to_file(self):
        write_test_soi_file("testInstance.soi")
        instance = OrdinalInstance("testInstance.soi")
        instance.write("testInstance_new.soi")
        with open("testInstance.soi", "r", encoding="utf-8") as init_file:
            init_file_content = init_file.read()
        os.remove("testInstance.soi")
        with open("testInstance_new.soi", "r", encoding="utf-8") as new_file:
            new_file_content = new_file.read()
        os.remove("testInstance_new.soi")
        assert init_file_content == new_file_content
