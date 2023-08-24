import os
from unittest import TestCase

from preflibtools.instances import OrdinalInstance
from tests.instance.io.write_file_test import write_test_toi_file


class TestToiInstance(TestCase):
    def test_read_from_file(self):
        write_test_toi_file("testInstance.toi")
        instance = OrdinalInstance("testInstance.toi")
        assert instance.orders[0] == ((3,), (1,), (2, 4))
        assert instance.orders[3] == ((3, 2, 1), (4,))
        assert instance.orders[4] == ((3, 2), (4, 1))
        os.remove("testInstance.toi")

    def test_write_to_file(self):
        write_test_toi_file("testInstance.toi")
        instance = OrdinalInstance("testInstance.toi")
        assert instance.data_type == "toi"
        instance.write("new_testInstance")
        assert os.path.isfile("new_testInstance.toi")
        os.remove("testInstance.toi")
        os.remove("new_testInstance.toi")
