import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def openXL(filename: str):
    filepath = f"data/sorted_excels/{filename}"
    df = pd.read_excel(filename)
    return df


if __name__ == "__main__":
    df = openXL("insulin_mortality_odds_ratio.xlsx")
