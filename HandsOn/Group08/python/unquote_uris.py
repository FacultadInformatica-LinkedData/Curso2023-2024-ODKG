import pandas as pd
from urllib.parse import unquote

# Leer el archivo csv
df = pd.read_csv('csv/us-colleges-and-universities-final-with-links.csv')

# Decodificar las URIs
df['same-as_wikidata_country'] = df['same_as_wikidata_country'].apply(
    lambda x: unquote(x))

# Guardar el dataframe decodificado en un nuevo archivo csv
df.to_csv(
    'csv/us-colleges-and-universities-final-with-links-unquoted.csv', index=False)
