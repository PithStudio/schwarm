#!/usr/bin/env python
import re
import itertools
import sys

from sys import argv

import numpy
import scipy
import matplotlib

from numpy import ndarray
from scipy import spatial

import scipy.spatial.distance as distance
import scipy.cluster.hierarchy as hierarchy

import matplotlib.pyplot as pylab

class Schwarm:
    """

    This script/module(pending on development) is intended to allow simpler 
    access to the data processing capabilities of the numpy + scipy + 
    matplotlib stack.

    Provides
        A minimal interface through which data can be passed in and with a
        resulting graph/image returned

    Interface
    ---------

    hierarchical_clustering(data)
    dendrogram(data_array, metric='euclidean')
    heat_mapped_distance_matrix()

    Requirements
    ------------

    This module will not function properly without the following installed:
    
    numpy
    scipy
    matplotlib

    Attributes
    ----------
    data_array : The array of the data we are clustering
    transpose_data_array : The trasnpose of the data_array
    names : The names of rows in the data
    columns : The column headers of the data

    

    """

    def __init__(self, data=[], row_names=[], column_headers=[]):
        self.__data_array = numpy.array(data)
        self.__transpose_data_array = self.__data_array.transpose()
        self.__names = numpy.array(row_names)
        self.__columns = numpy.array(column_headers)

    
    def heat_map(self):
        """
        Compute the heat map of a numpy.ndarray.

        Keyword arguments:
        data_array -- the numpy.ndarray
        """
        vmax = data_array.max()
        vmin = data_array.min()
        vmax = max([vmax, abs(vmin)])
        vmin = vmax * -1
        norm = mpl.colors.Normalize(vmin/2, vmax/2)

    def hierarchical_clustering(self):
        """
        Take in a data set in the form of a numpy.ndarray then graph the 
        information after performing hierarchical clustering, computing the
        dendrograms for both axis and generating a heatmap for the distance matrix.

        """
        data_x_array = numpy.array(data)
        try:
            color_map = getattr(pylab.cm, color_gradient)
        except AttributeError:
            color_map = color_map(color_gradient)

        (x_dendrogram_dictionary, x_linkage, x_leaves_list) = dendrogram(self.__data_array)
        (y_dendrogram_dictionary, y_linkage, y_leaves_list) = dendrogram(self.__transpose_data_array)

    def color_map(self):
        """
        Generate a Color map based on the input list

        Keyword arguments:
        gradient_list -- A list of colors to map by

        Example: ['red', 'blue', 'black']
        """
        print "That colormap doesn't exist yet"
        sys.exit()

    def dendrogram(self, data_array, metric='euclidean'):
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

        return (dendrogram_dict, linkage_matrix, heat_map_order)

    


    # data_array = numpy.array(data)

    # hierarchical_clustering(data_array)

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

test_schwarm = Schwarm(data, names, column_headers)
