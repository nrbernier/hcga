# -*- coding: utf-8 -*-
# This file is part of hcga.
#
# Copyright (C) 2019, 
# Robert Peach (r.peach13@imperial.ac.uk), 
# Alexis Arnaudon (alexis.arnaudon@epfl.ch), 
# https://github.com/ImperialCollegeLondon/hcga.git
#
# hcga is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# hcga is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with hcga.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import networkx as nx

class ShortestPaths():
    """
    Shortest path class
    """
    def __init__(self, G):
        self.G = G
        self.feature_names = []
        self.features = {}

    def feature_extraction(self):

        """Compute the various shortest path measures.

        Parameters
        ----------
        G : graph
           A networkx graph

        Returns
        -------
        feature_list :list
           List of features related to shortest paths.


        Notes
        -----
        Shortest path calculations using networkx:
            `Networkx_shortestpaths <https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.shortest_path.html#networkx.algorithms.shortest_paths.generic.shortest_path>`_
        
        There may be more than one shortest path between a source and target.
        This computes features on one of them.

        """
        

        
        G = self.G

        feature_list = {}

        # Calculating the shortest paths stats
        shortest_paths = nx.shortest_path(G)

        # finding the mean and max shortest paths        
        shortest_path_length_mean = []
        shortest_path_length_max = []

        for i in G.nodes():
            shortest_path_length = []
            sp = list(shortest_paths[i].values())
            
            for j in range(len(sp)):
                shortest_path_length.append(len(sp[j]))
                
            shortest_path_length_mean.append(np.mean(shortest_path_length))
            shortest_path_length_max.append(np.max(shortest_path_length))

        feature_list['path_length_mean']=np.mean(shortest_path_length_mean)
        feature_list['path_length_mean_max']=np.mean(shortest_path_length_max)        
        feature_list['path_length_max']=np.max(shortest_path_length_max)       


        self.features = feature_list
