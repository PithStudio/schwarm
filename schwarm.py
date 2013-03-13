import numpy
import scipy
import matplotlib
import re
import itertools

from sys import argv
from numpy import ndarray
from scipy import spatial

import scipy.spatial.distance as distance
import scipy.cluster.hierarchy as hierarchy

import matplotlib.pyplot as plt

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
for entry in data:
    line = name_file.readline()
    if entry != []:
        line = line[0:line.find('\t')]
        names.append(line)
        
while [] in data:
    data.remove([])

column_file = open(argv[3], "rbU")

column_headers = []
for line in column_file:
    if line.find("subsetID") == -1:
        tab_index = line.find('\t')
        column_headers.append(line[0:tab_index])

data_array = numpy.array(data)
distance_matrix = distance.pdist(data_array, 'euclidean')
distance_square_matrix = distance.squareform(distance_matrix)

linkage_matrix = hierarchy.linkage(distance_square_matrix)

heat_map_order = hierarchy.leaves_list(linkage_matrix)

dendrogram_dict = hierarchy.dendrogram(linkage_matrix)

plt.show()
