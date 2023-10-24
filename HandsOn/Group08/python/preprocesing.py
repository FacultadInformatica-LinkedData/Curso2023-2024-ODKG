import pandas as pd

# PATHS CSVS


def change_path(filename): return filename.replace(
    "-updated.csv", "-final.csv")


BASE_PATH = "csv/"
UNIVERISTY_INFO_PATH = BASE_PATH + "us-colleges-and-universities-updated.csv"
UNIVERITY_RATES_PATH = BASE_PATH + "IPEDS-data-updated.csv"
COLLEGE_RANKING = BASE_PATH + \
    "US-News-Rankings-Liberal-Arts-Colleges-Through-2023-updated.csv"
UNIVERSITY_ARTS_RANKING = BASE_PATH + \
    "US-News-Rankings-Universities-Through-2023-updated.csv"

# Preprocesing
# Eliminar duplicados

df_ranks = pd.read_csv(UNIVERISTY_INFO_PATH)

duplicados = df_ranks['IPEDSID'].duplicated(keep=False)
print("Number of dups", len(df_ranks[duplicados]))
print("Old:", len(df_ranks))

df_ranks.drop_duplicates(subset="IPEDSID", keep="last", inplace=True)


print("New:", len(df_ranks))
print(df_ranks.keys())


# Poner los valores de las columnas en un formato adecuado para poder realizar el mapping

columns_to_title_case = ['NAME', 'CITY']
df_ranks[columns_to_title_case] = df_ranks[columns_to_title_case].apply(
    lambda x: x.str.title())

df_ranks['COUNTRY'] = 'United States'

df_ranks.to_csv(change_path(UNIVERISTY_INFO_PATH), index=False)


##

df_rates = pd.read_csv(UNIVERITY_RATES_PATH)

duplicados = df_ranks['IPEDSID'].duplicated(keep=False)
print("Number of dups", len(df_ranks[duplicados]))

df_rates.to_csv(change_path(UNIVERITY_RATES_PATH))


# Preprocesado sergio

df_ranking_college = pd.read_csv(COLLEGE_RANKING)
df_ranking_college = df_ranking_college.melt(
    id_vars=['IPEDSID'], var_name='Year', value_name='Ranking')
df_ranking_college.to_csv(change_path(COLLEGE_RANKING), index=False)

# Preprocesado adri

df_ranking_university = pd.read_csv(UNIVERSITY_ARTS_RANKING)
df_ranking_university = df_ranking_university.melt(
    id_vars=['IPEDSID'], var_name='Year', value_name='Ranking')
df_ranking_university.to_csv(change_path(UNIVERSITY_ARTS_RANKING), index=False)
