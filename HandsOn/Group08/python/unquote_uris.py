import pandas as pd
from urllib.parse import unquote

# Leer el archivo csv
df = pd.read_csv('csv/us-colleges-and-universities-final-with-links.csv')

# Decodificar las URIs
df['same_as_wikidata_country'] = df['same_as_wikidata_country'].str.replace(
    'https://wikidata.org/entity/', '')

df['same_as_wikidata_city'] = df['same_as_wikidata_city'].str.replace(
    'https://wikidata.org/entity/', '')

df['same_as_wikidata_state'] = df['same_as_wikidata_state'].str.replace(
    'https://wikidata.org/entity/', '')

df['same_as_wikidata_name'] = df['same_as_wikidata_name'].str.replace(
    'https://wikidata.org/entity/', '')


df.to_csv(
    'csv/us-colleges-and-universities-final-with-links-unquoted.csv', index=False)
