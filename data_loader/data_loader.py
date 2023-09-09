from enum import Enum
from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd

import numpy as np



def parse_line(line: str, dtypes: Dict[str, List[str]]):
    line_split = line.strip().split(":")
    type_info = line_split[1].split(",")
    type_info[-1] = type_info[-1].strip(".")
    dtypes[line_split[0]] = type_info.copy()
    return line_split[0], dtypes


class CrossValType(Enum):
    FullSample = 0
    CrossValidation = 1
    StratifiedCrossValidation = 2

class DataLoader:
    def __init__(self):
        return
    
    @staticmethod
    def load(data_path: Path) -> Tuple[pd.DataFrame, Dict[str, List[str]]]:
        assert data_path.is_dir(), "Please provide directory path containing *.data, *.info, *.names files"
        dp = data_path.joinpath(f"{data_path.stem}.data")
        names = data_path.joinpath(f"{data_path.stem}.names")
        data_types = {}
        with open(names, "r") as name_file:
            column_names, dtypes = zip(*[parse_line(line, dtypes = data_types) for line in name_file.readlines()[2:]])
        column_names = list(column_names)
        column_names.append("class")
        return pd.read_csv(dp, header=None, names=column_names), dtypes
    

    @staticmethod
    def partition(dataset: pd.DataFrame, cross_val_type: CrossValType) -> Tuple[pd.DataFrame, pd.DataFrame]:
        np.random.seed(12345)
        # shuffled_data = dataset.copy()
        # np.random.shuffle(shuffled_data)
        shuffled_data = dataset.sample(frac=1)
        shuffled_data.reset_index(drop=True)
        split = int(np.floor(len(shuffled_data) / 5))
        return shuffled_data.iloc[:split], shuffled_data.iloc[split:]
    
if __name__ == "__main__":
    df, dtypes = DataLoader.load(Path("../440data/voting"))
    print(df)
    print(dtypes)