from data_loader.data_loader import DataLoader
from metrics.metric import *

import unittest



import numpy as np
import pandas as pd


class TestMetric(unittest.TestCase):
    
    def setUp(self) -> None:
        self.data = pd.DataFrame(
            {
                "fur" : [1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
                "class": [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
            }
        )
        self.ig_gain_data = pd.DataFrame({ "outlook": [
                           "sunny", "sunny", "overcast", "rain", 
                           "rain", "rain", "overcast", "sunny", 
                           "sunny", "rain", "sunny", "overcast", 
                           "overcast", "rain"
                        ], "temperature": [
                            "hot", "hot", "hot", "mild",
                            "cool", "cool", "cool", "mild",
                            "cool", "mild", "mild", "mild", 
                            "hot", "mild"
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
        self.metric = Metric()
        self.ig = InfoGain()
        return super().setUp()

    def test_entropy(self):
        self.assertAlmostEqual(0.94, self.metric.entropy(self.data["class"]), places=2)
        return
    
    def test_info_gain(self):
        test_igs = dict(
            outlook = 0.247,
            humidity = 0.152,
            wind = 0.048,
            temperature = 0.029,
        )
        igs = self.ig.calculate(self.ig_gain_data)
        for key in test_igs.keys():
            self.assertAlmostEqual(test_igs[key], igs[key], places=3)
        return
    
    def test_gain_ratio(self):
        # self.assertAlmostEqual()
        return