from __future__ import annotations

"""
Custom Libraries
"""
from data_loader.data_loader import DataLoader, CrossValType
from metrics.metric import *

"""
Standard Libraries
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

"""
3rd Party Libraries
"""
import pandas as pd

@dataclass
class Node:
    name: str
    value: Any
    parent: Node
    children: Dict[Any, Node]

@dataclass
class Classification:
    """
    Handy container
        classification_path: ordered list of attributes used to classify instance
        cls: classification determined by the decision tree
    """
    classification_path: List[str]
    cls: Union[int, str]


class Tree:
    def __init__(self, 
                 data_path: Path, 
                 max_depth: int, 
                 cross_validation: CrossValType, 
                 metric: Metric):
        assert data_path.exists(), "Please provide a valid path to data"
        assert max_depth >= 0, "Please provide a max depth integer >= 0"
        self._nodes = {}
        self.data_path = data_path
        self.max_depth = max_depth
        self.cross_validation = cross_validation
        self.metric = metric

        self.data, types = DataLoader.load(self.data_path)
        self.train_data, self.test_data = DataLoader.partition(self.data, cross_validation)
        return
    
    def build_tree(self, data: pd.DataFrame):
        print(f"Building the decision tree... with {data.shape}")

        self._build(0, self._nodes, data)
        return
    
    def _build(self, current_depth: int, current_tree_level: Dict, dataset: pd.DataFrame):
        if len(dataset.columns) == 1 or (current_depth >= self.max_depth and self.max_depth > 0):
            current_tree_level["class"] = dataset["class"].value_counts().idxmax()
            return
        
        metric_vals = self.metric.calculate(dataset)
        next_node = max(metric_vals.items(), key=lambda k: k[1])
        column_name = next_node[0]
        print(f"Next column to process: {column_name}")
        valid_columns = lambda: dataset.columns.difference([column_name], sort=False)
        current_tree_level[column_name] = {}
        next_depth = current_depth + 1
        for attr_val in dataset[column_name].unique():
            current_tree_level[column_name][attr_val] = {}
            self._build(next_depth, current_tree_level[column_name][attr_val], 
                        dataset=dataset.loc[dataset[column_name] == attr_val][valid_columns()])
        return
    
    def train(self):
        self.build_tree(self.train_data)
        return
    
    def test(self) -> pd.DataFrame:
        return

    def classify(self, new_instance: pd.DataFrame) -> Classification:
        first_key = list(self._nodes.keys())[0]
        instance_value = new_instance[first_key]
        current_level = current_level[instance_value]
        classification = self._classify(current_level, new_instance)
        return classification
    
    def visualize(self):
        return
    
    def _classify(self, level: Dict, new_instance: pd.DataFrame) -> Classification:
        return
    
    @property
    def nodes(self):
        return self._nodes.copy()