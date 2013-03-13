import numpy
import scipy
import matplotlib
from numpy import ndarray
<<<<<<< HEAD
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
=======

print(
    numpy.array([
        [1.2, 3.4, 6.7],
        [84.3, 29.3, 38.1]],
    numpy.dtype(float)))
>>>>>>> origin/HEAD
