import pandas as pd

from globals import UNIVERISTY_INFO, UNIVERSITY_ARTS_RANKING

df_unis = pd.read_csv(UNIVERISTY_INFO)

df_ranking = pd.read_csv(UNIVERSITY_ARTS_RANKING)


set_1 = set(df_ranking["IPEDSID"])
set_2 = set(df_unis["IPEDSID"])

print("Same:",len(set_1 and set_2))
print("Diff:", len(set_1 - set_2))