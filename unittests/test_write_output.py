from unittest import TestCase
from src.h1b_certified_stats import write_output, get_original_data
import csv
import os

class TestWrite_output(TestCase):

    def test_write_output_file_not_data(self):
        data = dict()
        field_name = 'occupancy'
        outfile = os.path.dirname(__file__)+"/output/out.txt"
        reader = csv.reader(data, quotechar='"')
        write_output(data, field_name, outfile, 10)

        cnt = 0
        for rec in reader:
            cnt+1

        self.assertEqual(cnt, 0)

    def test_write_output_file_divide_zero(self):
        f = os.path.dirname(__file__)+"/input/source.csv"
        outfile = os.path.dirname(__file__)+"/output/out.txt"
        occupations_dict, states_dict, certified_count = get_original_data(f, ";")
        write_output(occupations_dict, "OCC", outfile, 0)
