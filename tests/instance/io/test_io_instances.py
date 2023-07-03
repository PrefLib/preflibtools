from unittest import TestCase

import os

from preflibtools.instances import *
from tests.instance.io.write_file_test import write_test_soi_file, write_test_cat_file


class TestAnalysis(TestCase):

    def test_read_errors(self):
        write_test_soi_file("testInstance.soi")
        instance = PrefLibInstance()
        with self.assertRaises(TypeError):
            instance.parse_file("testInstance.soi")
        os.remove("testInstance.soi")

        write_test_cat_file("testInstance.cat")
        instance = PrefLibInstance()
        with self.assertRaises(TypeError):
            instance.parse_file("testInstance.cat")
        os.remove("testInstance.cat")

