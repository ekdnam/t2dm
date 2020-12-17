import pandas as pd
import os
import pickle

__MEDICAL_PARAMS__ = ["insulin", "mortality", "hazard_ratio"]
__FILENAME__ = "insulin_mortality_hazard_ratio.xlsx"

__FILEPATH__ = f"data/sorted_excels/{__FILENAME__}"

df = pd.read_excel(__FILEPATH__)

print(df)

pmids = df["PMID"]
titles = df["Title"]

args = ["is_downloaded", "cannot_be_downloaded"]

queries = []

for pmid, title in zip(pmids, titles):
	query = f"db.imhr.insert({{pmid: {pmid}, title: \"{title}\", insulin: 1, mortality: 1, hazard_ratio: 1, is_downloaded: 0, cannot_be_downloaded: 0}})"
	queries.append(query)
	print(query)

# with open('scratch/insulin_mortality_hazard_ratio.txt', 'w') as f:
#     for query in queries:
#         f.write("%s\n" % str(query))

with open('scratch/insulin_mortality_hazard_ratio.txt', 'wb') as fp:
    pickle.dump(queries, fp)