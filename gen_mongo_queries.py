import pandas as pd
import os
import pickle

__MEDICAL_PARAMS__ = ["insulin", "mortality", "hazard_ratio"]
__FILENAME__ = "insulin_mortality_hazards_ratio.xlsx"
__FILEPATH__ = f"data/sorted_excels/{__FILENAME__}"

df = pd.read_excel(__FILEPATH__)

print(df)

pmids = df["PMID"]
titles = df["Title"]

args = ["is_downloaded", "cannot_be_downloaded"]

queries = []

for pmid, title in zip(pmids, titles):
    query = f'db.allData.insert({{pmid: {pmid}, title: "{title}", insulin: 1, mortality: 1, hazards_ratio: 1, is_downloaded: 0, cannot_be_downloaded: 0}})'
    queries.append(query)
    print(query)
