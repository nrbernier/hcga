"""functions to extract features from graphs"""
import multiprocessing
import time
from importlib import import_module
from pathlib import Path
import networkx as nx
import numpy as np
from tqdm import tqdm

import pandas as pd


def extract(graphs, n_workers, mode="fast"):
    """main function to extract features"""

    feat_classes = get_list_feature_classes(mode)
    raw_features = compute_all_features(graphs, feat_classes, n_workers=n_workers)
    features, features_info = gather_features(raw_features, feat_classes)

    print(len(features.columns), "feature extracted.")
    good_features = filter_features(features)
    print(len(good_features.columns), "good features")
    return features, features_info


def _load_feature_class(feature_name):
    """load the feature class from feature name"""
    feature_module = import_module("hcga.features." + feature_name)
    return getattr(feature_module, feature_module.featureclass_name)


def get_list_feature_classes(mode="fast"):
    """Generates and returns the list of feature classes to compute for a given mode"""
    feature_path = Path(__file__).parent / "features"
    non_feature_files = ["__init__", "feature_class"]

    list_feature_classes = []
    trivial_graph = nx.generators.classic.complete_graph(3)

    for f_name in feature_path.glob("*.py"):
        feature_name = f_name.stem
        if feature_name not in non_feature_files:
            feature_class = _load_feature_class(feature_name)
            if mode in feature_class.modes or mode == "all":
                list_feature_classes.append(feature_class)
                # runs once update_feature with trivial graph to create class variables
                feature_class(trivial_graph).update_features({})
    return list_feature_classes


class Worker:
    """worker for computing features"""

    def __init__(self, list_feature_classes):
        self.list_feature_classes = list_feature_classes

    def __call__(self, graph):
        return feature_extraction(graph, self.list_feature_classes)


def feature_extraction(graph, list_feature_classes, with_runtimes=False):
    """extract features from a single graph"""

    if with_runtimes:
        runtimes = {}

    all_features = {}
    for feature_class in list_feature_classes:
        if with_runtimes:
            start_time = time.time()

        feature_inst = feature_class(graph)
        feature_inst.update_features(all_features)

        if with_runtimes:
            runtimes[feature_class.shortname] = time.time() - start_time

    if with_runtimes:
        return all_features, runtimes
    return all_features


def compute_all_features(graphs, list_feature_classes, n_workers=1):
    """compute the feature from all graphs"""
    print("Computing features for {} graphs:".format(len(graphs)))

    worker = Worker(list_feature_classes)

    if n_workers == 1:
        mapper = map
    else:
        pool = multiprocessing.Pool(n_workers)
        mapper = pool.imap

    return list(tqdm(mapper(worker, graphs), total=len(graphs)))


def gather_features(all_features_raw, list_feature_classes):
    """convert the raw feature to a pandas dataframe and a dict with features infos"""

    features_info = {}
    all_features = {}

    for feature_class in list_feature_classes:
        feature_inst = feature_class()

        for feature in all_features_raw[0][feature_inst.shortname]:
            feature_info = feature_inst.get_feature_info(feature)
            features_info[feature_info["feature_name"]] = feature_info

            all_features[feature_info["feature_name"]] = []
            for i, _ in enumerate(all_features_raw):
                all_features[feature_info["feature_name"]].append(
                    all_features_raw[i][feature_inst.shortname][feature]
                )

    return pd.DataFrame.from_dict(all_features), features_info


def filter_features(features):
    """filter features and create feature matrix"""

    # remove inf and nan
    features.replace([np.inf, -np.inf], np.nan)
    valid_features = features.dropna(axis=1)

    # remove features with equal values accros graphs
    return valid_features.drop(
        valid_features.std()[(valid_features.std() == 0)].index, axis=1
    )
