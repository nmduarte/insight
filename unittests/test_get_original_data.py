from unittest import TestCase
from src.h1b_certified_stats import get_original_data
import os


class TestGet_original_data(TestCase):

    def test_get_original_data_just_headers(self):
        f = os.path.dirname(__file__)+"/input/source_just_headers.csv"
        occupations_dict, states_dict, certified_count = get_original_data(f, ";")
        self.assertTrue(len(occupations_dict) == 0 and len(states_dict) == 0 and certified_count == 0)

    def test_get_original_data_different_case_headers(self):
        f = os.path.dirname(__file__)+"/input/source_different_headers.csv"
        occupations_dict, states_dict, certified_count = get_original_data(f, ";")
        self.assertTrue(len(occupations_dict) > 0 and len(states_dict) > 0 and certified_count > 0)

    def test_get_original_data_missing_headers(self):
        with self.assertRaises(SystemExit):
            f = os.path.dirname(__file__)+"/input/source_missing_headers.csv"
            get_original_data(f, ";")

    def test_get_original_data_not_available_data(self):
        f = os.path.dirname(__file__)+"/input/source_not_available_data.csv"
        occupations_dict, states_dict, certified_count = get_original_data(f, ";")

        cntStates, cntOcc = 0, 0

        for key, item in states_dict.items():
            if key == 'N/A':
                cntStates += 1

        for key, item in occupations_dict.items():
            if key == 'N/A':
                cntOcc += 1

        self.assertEqual(cntStates, 1)
        self.assertEqual(cntOcc, 1)
