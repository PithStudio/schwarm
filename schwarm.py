import numpy
import scipy
import matplotlib
from numpy import ndarray
import re
from sys import argv

nan = re.compile('NaN')

data_file = open(argv[1], "rbU")

data = []
for line in data_file:
    data_row = []
    if nan.search(line) is None:
        tab_index = line.find('\t')
        while tab_index != -1:
            data_row.append(float(line[0:tab_index]))
            line = line[tab_index + 1:]
            tab_index = line.find('\t')
        data_row.append(float(line))
    data.append(data_row)

name_file = open(argv[2], "rbU")

names = []
for line in name_file:
    if line.find("sampleID") == -1:
        tab_index = line.find('\t')
        names.append(line[0:tab_index])

column_file = open(argv[3], "rbU")

column_headers = []
for line in column_file:
    if line.find("subsetID") == -1:
        tab_index = line.find('\t')
        column_headers.append(line[0:tab_index])
