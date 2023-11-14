import pandas as pd
from globals import UNIVERISTY_INFO, UNIVERITY_RATES, UNIVERSITY_ARTS_RANKING, COLLEGE_RANKING
from globals import change_path

# Preprocesing

## UNIVERISTY_INFO

### Eliminar duplicados

df_ranks = pd.read_csv(UNIVERISTY_INFO)

duplicados = df_ranks['IPEDSID'].duplicated(keep=False)
print("Number of dups", len(df_ranks[duplicados]))
print("Old:", len(df_ranks))

df_ranks.drop_duplicates(subset="IPEDSID", keep="last", inplace=True)

print("New:", len(df_ranks))
print(df_ranks.keys())


### Poner los valores de las columnas en un formato adecuado para poder realizar el mapping

columns_to_title_case = ['NAME', 'CITY']
df_ranks[columns_to_title_case] = df_ranks[columns_to_title_case].apply(
    lambda x: x.str.title())

df_ranks['COUNTRY'] = 'United States'

df_ranks.to_csv(change_path(UNIVERISTY_INFO), index=False)


# UNIVERITY_RATES

df_rates = pd.read_csv(UNIVERITY_RATES)

duplicados = df_ranks['IPEDSID'].duplicated(keep=False)
print("Number of dups", len(df_ranks[duplicados]))

df_rates.to_csv(change_path(UNIVERITY_RATES))


## COLLEGE_RANKING

df_ranking_college = pd.read_csv(COLLEGE_RANKING)
df_ranking_college = df_ranking_college.melt(
    id_vars=['IPEDSID'], var_name='Year', value_name='Ranking')
df_ranking_college.to_csv(change_path(COLLEGE_RANKING), index=False)

## UNIVERSITY_ARTS_RANKING

df_ranking_university = pd.read_csv(UNIVERSITY_ARTS_RANKING)
df_ranking_university = df_ranking_university.melt(
    id_vars=['IPEDSID'], var_name='Year', value_name='Ranking')
df_ranking_university.to_csv(change_path(UNIVERSITY_ARTS_RANKING), index=False)
