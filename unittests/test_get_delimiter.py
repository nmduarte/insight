from unittest import TestCase
from src.h1b_certified_stats import get_delimiter
import os

class TestGet_delimiter(TestCase):

    def test_get_delimiter_semicolumn(self):
        f = os.path.dirname(__file__)+"/input/source.csv"
        dlm = get_delimiter(f)
        self.assertEqual(dlm, ";")

    def test_get_delimiter_tab(self):
        f = os.path.dirname(__file__) + "/input/source_tab_delimited.csv"
        dlm = get_delimiter(f)
        self.assertEqual(dlm, "\t")
