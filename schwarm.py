#!/usr/bin/python
"""
Schwarm
=======

This script/module(pending on development) is intended to allow simpler access
to the data processing capabilities of the numpy + scipy + matplotlib stack.

Provides
    A minimal interface through which data can be passed in and with a
    resulting graph/image returned

Interface
=======

hierarchical_clustering(data)
dendrogram(data_array, metric='euclidean')
heat_mapped_distance_matrix()

"""
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

import matplotlib.pyplot as pylab

def hierarchical_clustering(data):
    """
    Take in a data set in the form of a numpy.ndarray then graph the 
    information after performing hierarchical clustering, computing the
    dendrograms for both axis and generating a heatmap for the distance matrix.

    Keyword arguments:
    data -- the numpy.ndarray

    """
    data_x_array = numpy.array(data)
    x_dendrogram_dictionary = dendrogram(data_x_array)
    y_dendrogram_dictionary = dendrogram(data_x_array.transpose())


def dendrogram(data_array, metric='euclidean'):
    """
    Compute the dendrogram dictionary of a numpy.ndarray according to the given
    metric.

    Keyword arguments:
    data_array -- the numpy.ndarray
    metric -- the metric used to compute the dendrogram
    """
    distance_matrix = distance.pdist(data_array, metric)
    
    distance_square_matrix = distance.squareform(distance_matrix)
    linkage_matrix = hierarchy.linkage(distance_square_matrix)
    heat_map_order = hierarchy.leaves_list(linkage_matrix)
    dendrogram_dict = hierarchy.dendrogram(linkage_matrix)

    return dendrogram_dict

def heat_map():
    """
    Compute the heat map of a numpy.ndarray.
    """
    


if __name__ = '__main__':

    nan = re.compile('NaN')

    # Take in 3 files from the Command Line

    data_file = open(argv[1], "rbU") # The Tab delimited data file 

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
    data_file.close()

    name_file = open(argv[2], "rbU") # The Tab delimited file with x columns

    names = []
    for entry in data:
        line = name_file.readline()
        if entry != []:
            line = line[0:line.find('\t')]
            names.append(line)
    name_file.close()
            
    while [] in data:
        data.remove([])

    column_file = open(argv[3], "rbU") # The Tab delimited file with y columns

    column_headers = []
    for line in column_file:
        if line.find("subsetID") == -1:
            tab_index = line.find('\t')
            column_headers.append(line[0:tab_index])
    column_file.close()

    data_array = numpy.array(data)

    hierarchical_clustering(data_array)


