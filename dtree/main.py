from argparse import ArgumentParser, Namespace
from pathlib import Path
import numpy as np

def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", type=Path, help="Path to data")
    parser.add_argument("-c", "--cv", type=bool, action="store_true", help="Cross-validation or full sample")
    parser.add_argument("-d", "--depth", type=int, help="Maximum depth of decision tree")
    parser.add_argument("-i", "--info-gain", type=bool, action="store_true")
    return parser.parse_args()

def main():
    """
    1. Load data
    2. 
    """
    seed = np.random.seed(12345)
    
    return

if __name__ == "__main__":
    main()