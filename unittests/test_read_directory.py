import os
from unittest import TestCase
from src.h1b_certified_stats import read_directory


class TestRead_directory(TestCase):

    def setUp(self):
        self.files = read_directory(os.path.dirname(__file__)+"/input/one_file_only")

    def test_read_directory(self):
        self.assertTrue(type(self.files) is list)

    def test_multiple_files(self):
        open(os.path.dirname(__file__)+'/input/one_file_only/tmp.txt', 'a').close()
        self.assertRaises(SystemExit)
        os.remove(os.path.dirname(__file__)+'/input/one_file_only/tmp.txt')
