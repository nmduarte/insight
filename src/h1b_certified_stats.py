#!/usr/bin/env python

import csv
import os
import sys
import re
import logging
import argparse


def read_directory(path):
    """Read Input Directory folder

    Function to read the input directory and extract all the names of the existing files.
    Process can only deal with one csv at the time, so if more are found an error message is shown an system exits
    :param path: contains the path to the input folder
    :return: the name of the csv that is going to be processed
    """
    # gets the files names - for now just one, but in the future might be multiple. We only accept txt and csv files
    files = [os.path.join(path, f) for f in os.listdir(path) if f[-4:] == '.csv' or f[-4:] == '.txt']

    # for now we only accept one file - check to se if there's exactly one file
    if len(files) > 1:
        sys.exit("ERROR: At the moment only 1 input file(.csv or .txt) is permitted. Please remove extra files")
    elif len(files) < 1:
        sys.exit("ERROR: Input file is missing. Please add an input file(.csv or .txt) to the input folder")

    return files


def get_original_data(csv_fname, delimiter):
    """Read original data

    Function that reads the original csv file containing the source data. In case that there's only one line, then it's
    assumed that the file is not correct and system exits
    :param csv_fname: name of the csv to be processed. This value is returned by the read_directory function
    :param delimiter: delimiter of the source file
    :return: two dictionaries with the data to output and the counter of total certified records
    """

    # create variables to store data
    occupations_dict = dict()  # dictionary for the occupations
    states_dict = dict()  # dictionary for the states
    certified_count = 0  # number of certified accounts
    cnt = 0  # counter for lines stat

    with open(csv_fname, "r") as original_data:
        # reader for the csv input file
        reader = csv.reader(original_data, delimiter=delimiter, quotechar='"')

        # list with headers
        headers = next(reader)

        # tries to find the index of each field in the headers.
        # regex was used for the state since by looking at the different files, names could vary considerably, but
        # always contained WORK and STATE
        soc_name_index, status_index, state_index = None, None, None
        for idx, field in enumerate(headers):
            if 'SOC_NAME' in field.upper():
                soc_name_index = idx
            elif 'STATUS' in field.upper():
                status_index = idx
            elif re.search('.*WORK.*STATE', field.upper()):
                state_index = idx

        # tests if the 3 main columns are present
        if not all([soc_name_index, status_index, state_index]):
            sys.exit("ERROR: File does not have the required columns - Please make sure the source file has all columns "
                          "(soc name of the application, status of the application and state of the working place) "
                          "\nColumns should be separated by semi-columns")

        # gets the rest of the file and loads the values into the variables
        # if any of the variables is empty, then is marked as N/A and is outputted anyway so that can be visible
        # to whoever is looking at the output data
        for rec in reader:
            soc_name = rec[soc_name_index]
            status = rec[status_index]
            state = rec[state_index]
            if not soc_name.strip():
                soc_name = 'N/A'
            if not status.strip():
                status = 'N/A'
            if not state.strip():
                state = 'N/A'

            if status.upper() == "CERTIFIED":
                # increment count of certified applications
                certified_count += 1

                # add data points to dictionaries as values and their number as value
                if soc_name not in occupations_dict:
                    occupations_dict[soc_name] = 1
                else:
                    occupations_dict[soc_name] += 1
                if state not in states_dict:
                    states_dict[state] = 1
                else:
                    states_dict[state] += 1
            # just for log purposes
            cnt += 1

    logging.info('Read %s records in data file' % cnt)
    return occupations_dict, states_dict, certified_count


def write_output(data, field_name, outfile, certified_count):
    """ Function to write the output files

    This function creates the output files containing the final results

    :param data: dictionary containing the output data
    :param field_name: name of the header/data to be outputted
    :param outfile: name of the output file
    :param certified_count: number of certified records
    :return: output file
    """

    # create list of tuples by sorting dictionary first by value (number) descending,
    # then by value (occupation or state)
    data_sorted = sorted(data.items(), key=lambda x: (-x[1], x[0]))

    # opens file to write
    with open(outfile, 'w') as out_file:

        writer = csv.writer(out_file, delimiter=';', quotechar='"')

        # write header to output file
        writer.writerow([field_name, 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE'])

        # iterate over first 10 elements in sorted list
        for data_tuple in data_sorted[:10]:

            # calculate percentage
            if certified_count == 0:
                percentage = 0
            else:
                percentage = data_tuple[1] * 100 / certified_count

            # convert percentage to string, rounded to one decimal
            perc_str = "{0:.1f}%".format(percentage)

            # write to output file
            writer.writerow([data_tuple[0], data_tuple[1], perc_str])

        logging.info("Wrote records to file %s" % outfile)


def get_delimiter(input_file):
    """Function to get the delimiter of the source file

    :param input_file: input file containing the source data
    :return: delimiter of the input file
    """

    with open(input_file) as f:

        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(f.read())

    return dialect.delimiter


def main(parameters):
    """ Main function

    Main function - calls the functions to read and process the input file
    :return: None
    """

    # Check input/output dirs exist before processing data
    if not os.path.isdir(parameters.input):
        sys.exit("ERROR: Input folder does not exist.")

    if not os.path.isdir(parameters.output):
        sys.exit("ERROR: Output folder does not exist.")

    # read the name of the existing file in the input directory
    filenames = read_directory(parameters.input)

    # get delimiter in csv file
    delimiter = get_delimiter(filenames[0])

    # get data from input file
    occupations_dict, states_dict, certified_count = get_original_data(filenames[0], delimiter)

    # create output file for occupations
    write_output(occupations_dict, 'TOP_OCCUPATIONS', os.path.join(parameters.output, 'top_10_occupations.txt'),
                 certified_count)

    # create output file for state
    write_output(states_dict, 'TOP_STATES', os.path.join(parameters.output, 'top_10_states.txt'), certified_count)


if __name__ == '__main__':

    # inputs from console. defaults set to the input/output folder existing in the repo structure
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input',
                    default='./input',
                    help='Directory containing input files')
    ap.add_argument('-o', '--output',
                    default='./output',
                    help='Directory to store output files')

    cmd_opts = ap.parse_args()

    # set logging format
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s ', level=logging.INFO)

    main(cmd_opts)
