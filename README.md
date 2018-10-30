# Table of Contents
1. [Problem](README.md#problem)
2. [Approach](README.md#approach)
3. [Run Instructions](README.md#run-instructions)
4. [Output](README.md#output)

# Problem

A newspaper editor was researching immigration data trends on H1B(H-1B, H-1B1, E-3) visa application processing over the past years, trying to identify the occupations and states with the most number of approved H1B visas. She has found statistics available from the US Department of Labor and its [Office of Foreign Labor Certification Performance Data](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis). But while there are ready-made reports for [2018](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2018/H-1B_Selected_Statistics_FY2018_Q4.pdf) and [2017](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2017/H-1B_Selected_Statistics_FY2017.pdf), the site doesn’t have them for past years. 

As a data engineer, you are asked to create a mechanism to analyze past years data, specificially calculate two metrics: **Top 10 Occupations** and **Top 10 States** for **certified** visa applications.

Your code should be modular and reusable for future. If the newspaper gets data for the year 2019 (with the assumption that the necessary data to calculate the metrics are available) and puts it in the `input` directory, running the `run.sh` script should produce the results in the `output` folder without needing to change the code.

# Approach

The approach to the problem was to load the source file into two different dictionaries - one for occupations and other for the states. The total number of certified applications would be collected as well so that the final percentages can be calculated.

Each entry of the dictionary contains the occupation/state as key and the number of certified applications for that key as the value, making it pretty clear and simple to deal with that data. The percentages can then be calculated and be written to the output files

Script was created using Python3

# Run Instructions

The program receives two inputs: The input folder and the output folder. These folders need to exist prior to executing the program.

`python ./src/h1b_certified_stats.py --input ./inputFolder --output ./outputFolder`

If no parameters are provided, default folders are used:

* `./inputFolder`: Input folder for source data, under the root folder

* `./outputFolder`: Output folder for output data, under the root folder

For convenience, a  `run.sh` has been created. It can be executed in order to run the application.

* `cc~$ ./run.sh` 

# Output 

Two files are created as the output:

* `top_10_occupations.txt`: Contains the occupations that got more applications certified

* `top_10_states.txt`: Contains the states that got more applications certified

# Unit Testing

Unit tests were created and can be executed running the following command in the *root folder* of the project:

`python -m unittest discover unittests "test_*.py"`
