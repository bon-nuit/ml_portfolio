from data_loader.data_loader import DataLoader, CrossValType
from dtree.tree import *
from pathlib import Path
import unittest
import unittest.mock as mock

class TestDtree(unittest.TestCase):

    
    @mock.patch.object(DataLoader, "partition")
    @mock.patch.object(DataLoader, "load")
    def setUp(self, mock_data_loader, mock_data_partition):
        self.mock_path = mock.MagicMock()
        self.mock_val = mock.MagicMock()
        self.mock_metric = mock.MagicMock()
        self.depth = 5
        test_data = pd.DataFrame({
                                "day": range(1, 15), 
                                "outlook": [
                                    "sunny", "sunny", "overcast", "rain", 
                                    "rain", "rain", "overcast", "sunny", 
                                    "sunny", "rain", "sunny", "overcast", 
                                    "overcast", "rain"
                                ], "temperature": [
                                    95, 88, 85, 62,
                                    45, 42, 55, 72,
                                    49, 61, 72, 61, 
                                    81, 60
                                ], "humidity": [
                                    "high", "high", "high", "high",
                                    "normal", "normal", "normal", "high",
                                    "normal", "normal", "normal", "high",
                                    "normal", "high"
                                ], "wind": [
                                    "weak", "strong", "weak", "weak",
                                    "weak", "strong", "strong", "weak",
                                    "weak", "weak", "strong", "strong",
                                    "weak", "strong"
                                ], "class": [
                                    "no", "no", "yes", "yes",
                                    "yes", "no", "yes", "no",
                                    "yes", "yes", "yes", "yes",
                                    "yes", "no"
                                ]
                            })
        DataLoader.load.return_value = test_data, (int, str, int, str, str, str)
        DataLoader.partition.return_value = (test_data[:12], test_data[12:])
        self.tree = Tree(self.mock_path, self.depth, self.mock_val, self.mock_metric)
        return
    

    def test_output_dict(self):
        self.tree.train()
        self.assertIsInstance(self.tree.nodes, dict)
        return
    
    def test_correctly_built_tree(self):

        # correct_output = {}
        # tree = Tree(mock_path, 5, mock_val, mock_metric)
        # self.assertDictEqual(correct_output)
        return
    
    def test_stops_correct_depth(self):
        return
    
    def test_correctly_classifies(self):
        return
    
    def test_builds_history(self):
        return
    
    def test_prune(self):
        return
    
    def test_test_use_test_data(self):
        return
    
    def test_train_use_train_data(self):
        return