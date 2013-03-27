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
        if not data:
            print("Can not analyze an empty data set")
            sys.exit()
        self.__data_array = numpy.array(data)
        self.__transpose_data_array = self.__data_array.transpose()
        self.__names = numpy.array(row_names)
        self.__columns = numpy.array(column_headers)

    
    def set_color_map(self, color_gradient):
        """
        Set the color map to the specified gradient

        Keyword arguments:
        color_gradient -- the specific gradient to use either located within
        matplotlib.cm. **TODO** Implement custom gradients within color_map()
        """
        try:
            self.__color_map = getattr(pylab.cm, color_gradient)
        except AttributeError:
            self.__color_map = color_map(color_gradient)

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

    def heat_map(self):
        """
        Compute the heat map of a numpy.ndarray.

        Keyword arguments:
        data_array -- the numpy.ndarray
        """
        # Set scaling values for the colors
        vmax = self.__data_array.max()
        vmin = self.__data_array.min()
        vmax = max([vmax, abs(vmin)])
        vmin = vmax * -1
        norm = matplotlib.colors.Normalize(vmin/2, vmax/2)

        # Set scale of matplotlib window size
        default_window_height = 8.5
        default_window_width = 12
        fig = pylab.figure(
            figsize = (default_window_width, default_window_height))
        color_bar_w = 0.015 # width of colorbar

        # Set positions for all the elements that compose our final graphic
        # Set bearings of the leftmost dendrogram
        side_dendrogram_bearings = [0.05, 0.22, 0.2, 0.6]
        dist_side_dendro_side_colorbar = 0.004
        dist_side_dendro_top_colorbar = 0.004

        # Set bearings of the leftmost colorbar
        side_color_bar_bearings = [0.31, 0.1, color_bar_w, 0.6]
        side_color_bar_bearings[0] = (
            side_dendrogram_bearings[0] + side_dendrogram_bearings[2] + dist_side_dendro_side_colorbar)
        side_color_bar_bearings[1] = side_dendrogram_bearings[1]
        side_color_bar_bearings[2] = side_dendrogram_bearings[2]
        dist_side_colorbar_heatmap = 0.004

        # Set bearings of topmost colorbar
        top_color_bar_bearings = [0.4, 0.63, 0.5, color_bar_w]
        top_color_bar_bearings[0] = (
            side_color_bar_bearings[0] + color_bar_w + dist_side_colorbar_heatmap)
        top_color_bar_bearings[1] = (
            side_dendrogram_bearings[1] + side_dendrogram_bearings[3] + dist_side_dendro_side_colorbar)
        dist_top_dendro_top_colorbar = 0.004

        # Set bearings of heatmap
        heatmap_bearings = [0.3, 0.72, 0.6, 0.15]
        heatmap_bearings[0] = (
            side_color_bar_bearings[0] + side_color_bar_bearings[2] + dist_side_colorbar_heatmap)
        heatmap_bearings[1] = side_dendrogram_bearings[1]
        heatmap_bearings[2] = top_color_bar_bearings[3]
        heatmap_bearings[3] = side_dendrogram_bearings[3]

        # Set bearings of topmost dendrogram
        top_dendrogram_bearings = [0.3, 0.72, 0.6, 0.15]
        top_dendrogram_bearings[0] = (
            side_color_bar_bearings[0] + color_bar_w + dist_side_colorbar_heatmap)
        top_dendrogram_bearings[1] = (
            side_dendrogram_bearings[1] + side_dendrogram_bearings[3] + 
            dist_side_dendro_top_colorbar + color_bar_w + dist_top_dendro_top_colorbar)
        top_dendrogram_bearings[2] = top_color_bar_bearings[2]

        # Set bearings for the color legend
        color_legend_bearings = [0.07, 0.88, 0.18, 0.09]

        # Compute top dendrogram and plot its axes
        top_dendro_axes = fig.add_axes(top_dendrogram_bearings, frame_on=True)
        (top_dendro_dict, top_dendro_linkage, top_dendro_leaves) = self.dendrogram(self.__data_array)
        top_dendro_flat_cluster = hierarchy.fcluster(
            top_dendro_linkage, 0.7*max(top_dendro_linkage[:,2]), 'distance')
        top_dendro_axes.set_xticks([])
        top_dendro_axes.set_yticks([])

        # Compute side dendrogram and plot its axes
        side_dendro_axes = fig.add_axes(side_dendrogram_bearings, frame_on=True)
        (side_dendro_dict, side_dendro_linkage, side_dendro_leaves) = self.dendrogram(self.__data_array)
        side_dendro_flat_cluster = hierarchy.fcluster(
            side_dendro_linkage, 0.7*max(side_dendro_linkage[:,2]), 'distance')
        side_dendro_axes.set_xticks([])
        side_dendro_axes.set_yticks([])

        # plot axes of heatmap
        heatmap_axes = fig.add_axes(heatmap_bearings)
        data_array_t = self.__data_array

        # handle the top dendrogram's leaves
        top_dendro_leaves = top_dendro_dict['leaves']
        data_array_t = data_array_t[:,top_dendro_leaves]
        top_dendro_flat_cluster = top_dendro_flat_cluster[:,top_dendro_leaves]
        
        # handle the side dendrogram's leaves
        side_dendro_leaves = side_dendro_dict['leaves']
        data_array_t = data_array_t[side_dendro_leaves,:]
        side_dendro_flat_cluster = side_dendro_flat_cluster[side_dendro_leaves,:]
        
        # set coloring for heatmap
        heatmap_axes_img = heatmap_axes.matshow(
            self.__data_array, aspect='auto', origin='lower', cmap=self.__color_map, norm=norm)
        heatmap_axes.set_xticks([])
        heatmap_axes.set_yticks([])

        # Add column headers + row names
        new_names = []
        new_columns = []
        for i in range(self.__data_array.shape[0]):
            heatmap_axes.text(
                self.__data_array.shape[1]-0.5, i, '  '+self.__names[side_dendro_leaves[i]])
            new_names.append(self.__names[side_dendro_leaves[i]])
        for i in range(self.__data_array.shape[1]):
            if i == 36:
                break
            heatmap_axes.text(
                i, 
                -0.9, 
                ' '+self.__columns[top_dendro_leaves[i]], 
                rotation = 270, 
                verticalalignment = 'top')
            new_columns.append(self.__columns[top_dendro_leaves[i]])

        # set colors on the column side
        top_color_bar = fig.add_axes(top_color_bar_bearings)
        top_color_bar_colormap = matplotlib.colors.ListedColormap(
            ['r', 'g', 'b', 'y', 'w', 'k', 'm'])
        dc = numpy.array(top_dendro_flat_cluster, dtype = int)
        dc.shape = (1, len(top_dendro_flat_cluster))
        im_c = top_color_bar.matshow(
            dc, 
            aspect='auto', 
            origin='lower', 
            cmap=top_color_bar_colormap)
        top_color_bar.set_xticks([])
        top_color_bar.set_yticks([])

        # set colors on the row side
        side_color_bar = fig.add_axes(side_color_bar_bearings)
        side_color_bar_colormap = matplotlib.colors.ListedColormap(
            ['r', 'g', 'b', 'y', 'w', 'k', 'm'])
        dr = numpy.array(side_dendro_flat_cluster, dtype = int)
        dr.shape = (len(side_dendro_flat_cluster), 1)
        im_r = side_color_bar.matshow(
            dr,
            aspect='auto',
            origin='lower',
            cmap=side_color_bar_colormap)
        side_color_bar.set_xticks([])
        side_color_bar.set_yticks([])

        # plot color legend
        colorbar_axes = fig.add_axes(color_legend_bearings, frame_on = False)
        cb = matplotlib.colorbar.ColorbarBase(
            colorbar_axes, 
            cmap = self.__color_map, 
            norm = norm, 
            orientation = 'horizontal')
        colorbar_axes.set_title('colorkey')



        # set font size
        pylab.rcParams['font.size'] = 5

        pylab.show()

    def hierarchical_clustering(self):
        """
        Take in a data set in the form of a numpy.ndarray then graph the 
        information after performing hierarchical clustering, computing the
        dendrograms for both axis and generating a heatmap for the distance
        matrix.

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
test_schwarm.set_color_map('seismic')
test_schwarm.heat_map()