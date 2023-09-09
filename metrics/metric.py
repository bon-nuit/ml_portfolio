import enum
import numpy as np
import pandas as pd

from typing import Dict, List, Tuple, Union

class MetricID(enum.Enum):
    INFO_GAIN = 0
    GAIN_RATIO = 1

class Metric:
    def __init__(self):
        pass

    def calculate(self, df: pd.DataFrame) -> Dict[str, float]:
        print(f"wtf")
        pass

    def entropy(self, df: pd.DataFrame):
        probs = df.value_counts(normalize=True)
        log_probs = np.log2(probs)
        # print(f"Probs: {probs}")
        # print(f"Log probs: {log_probs}")
        entropy = -(probs @ log_probs).sum()
        return entropy
    
    def conditional_entropy(self, df: pd.DataFrame, group_by_col: str) -> float:
        probs_for_attributes = df[group_by_col].value_counts(normalize=True)
        # print(probs_for_attributes)
        current_entropy = 0.0
        for attr_value in df[group_by_col].unique():
            entropy_for_attr_val = self.entropy(df[["class", group_by_col]].loc[df[group_by_col] == attr_value])
            current_entropy += (probs_for_attributes[attr_value] * entropy_for_attr_val)
            
        # self.entropy(df[["class", group_by_col]].groupby(group_by_col))
        return current_entropy
    
class InfoGain(Metric):
    def __init__(self):
        return
    
    def calculate(self, df: pd.DataFrame) -> Dict[str, float]:
        class_entropy = self.entropy(df["class"]) #df.groupby("class").size().div(len(df)).sum()
        info_gains = {column: class_entropy - self.conditional_entropy(df, group_by_col=column) for column in df.columns if column != "class"}
        return info_gains #min(info_gains.items(), key=info_gains.get)
        cond_entro = -1.0
        for column in df.columns:
            cond_entro = max(cond_entro, self.conditional_entropy(df, group_by_col=column))
            current_ig = class_entropy - self.conditional_entropy(df, group_by_col=column)
            # p_class_given_column = pd.crosstab(df["class"], df[column], normalize="index")
            # neg_log_p = -np.log(p_class_given_column)
            # conditional_entropy = np.ma.masked_invalid(p_class_given_column * neg_log_p).sum(axis=1)
            
        return
    
class GainRatio(Metric):
    def __init__(self):
        self.ig = InfoGain()
        return
    
    def calculate(self, df: pd.DataFrame) -> Dict[str, float]:
        info_gains = self.ig.calculate(ig)
        gain_ratios = {attr: info_gains[attr] / self.entropy(df[attr]) for attr in df.columns if attr != "class"}
        return gain_ratios
    
if __name__ == "__main__":
    print(f"Version: {pd.__version__}")
    df = pd.DataFrame({"day": range(14), 
                       "outlook": [
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
    ig = InfoGain()
    print(ig.calculate(df))
    # # print(df)
    # class_entropy = df.groupby("class").size().div(len(df)) #.sum()
    # class_entropy *= -np.log(class_entropy)
    # class_entropy = class_entropy.sum()
    # print(f"Class entropy: {class_entropy}")
    # for column in df.columns:
    #     if column == "class":
    #         continue
    #     print(f"Calculating probs for {column}...")
    #     just_data = df.groupby(column).size().div(len(df))
    #     print(just_data)
    #     data = pd.crosstab(df["class"], df[column], normalize="index")
    #     print(data)
    #     log_data = -np.log(data)
    #     print(log_data)
    #     conditional_entropy = (data * log_data) #.sum(axis=1)
    #     print(f"{conditional_entropy}")
    #     conditional_entropy = conditional_entropy.sum(axis=0)
    #     print(f"{conditional_entropy}")
    #     # sums = np.ma.masked_invalid(conditional_entropy).sum(axis=1)
    #     # print(f"Sum is: {conditional_entropy}")
    #     conditional_entropy = just_data * conditional_entropy
    #     print(f"Info gain is: {class_entropy - conditional_entropy.sum()}")
