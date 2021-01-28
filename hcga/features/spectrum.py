"""Spectrum class."""
from functools import lru_cache, partial

import networkx as nx
import numpy as np

from hcga.feature_class import FeatureClass, InterpretabilityScore

featureclass_name = "Spectrum"


@lru_cache(maxsize=None)
def eval_spectrum_adj(graph):
    """"""
    return np.real(nx.linalg.spectrum.adjacency_spectrum(graph))


def eigenvalue_ratio(graph, i, j):
    """"""
    return eval_spectrum_adj(graph)[j] / eval_spectrum_adj(graph)[i]


@lru_cache(maxsize=None)
def eval_spectrum_modularity(graph):
    """"""
    return np.real(nx.linalg.spectrum.modularity_spectrum(graph))


@lru_cache(maxsize=None)
def eval_spectrum_laplacian(graph):
    """"""
    return np.real(nx.linalg.spectrum.laplacian_spectrum(graph))


class Spectrum(FeatureClass):
    """Spectrum class."""

    modes = ["medium", "slow"]
    shortname = "SPM"
    name = "spectrum"
    encoding = "networkx"

    def compute_features(self):

        # distribution of eigenvalues
        self.add_feature(
            "eigenvalues_adjacency",
            eval_spectrum_adj,
            "The summary statistics of eigenvalues of adjacency matrix",
            InterpretabilityScore(3),
            statistics="centrality",
        )

        # get ratio of eigenvalues
        n_eigs = 10
        for i in range(n_eigs):
            for j in range(i):
                self.add_feature(
                    "eigenvalue_ratio_{}_{}".format(i, j),
                    partial(eigenvalue_ratio, i=i, j=j),
                    "The ratio of the {} and {} eigenvalues".format(i, j),
                    InterpretabilityScore(2),
                )
        # distribution of eigenvalues
        self.add_feature(
            "eigenvalues_modularity",
            eval_spectrum_modularity,
            "The summary statistics of eigenvalues of modularity matrix",
            InterpretabilityScore(3),
            statistics="centrality",
        )

        # distribution of eigenvalues
        self.add_feature(
            "eigenvalues_laplacian",
            eval_spectrum_laplacian,
            "The summary statistics of eigenvalues of laplacian matrix",
            InterpretabilityScore(3),
            statistics="centrality",
        )
