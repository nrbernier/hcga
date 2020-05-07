"""Node clique number class."""
import networkx as nx
import numpy as np
from networkx.algorithms import clique

from ..feature_class import FeatureClass, InterpretabilityScore
from . import utils

featureclass_name = "NodeCliqueNumber"


class NodeCliqueNumber(FeatureClass):
    """Node clique number class."""

    modes = ["fast", "medium", "slow"]
    shortname = "CN"
    name = "node_clique_number"
    encoding = "networkx"

    def compute_features(self):
        """Compute the maximal clique containing each node, i.e passing through that node.

        Notes
        -----
        Clique number calculations using networkx:
            `Networkx_clique <https://networkx.github.io/documentation/stable/reference/algorithms/clique.html>`_
        """

        self.add_feature(
            "clique sizes",
            lambda graph: list(
                clique.node_clique_number(utils.ensure_connected(graph)).values()
            ),
            "the distribution of clique sizes",
            InterpretabilityScore(3),
            statistics="centrality",
        )
