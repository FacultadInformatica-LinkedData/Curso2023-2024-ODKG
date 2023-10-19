# %%Limpiar CSV Para que las columnas coincidan con los nombres de ciudades y universidades en DBPEDIA
import morph_kgc
import pandas as pd

csv = pd.read_csv('HandsOn/Group08/csv2/us-colleges-and-universities.csv')

columna = csv['NAME']
columna2 = csv['CITY']
columna3 = csv['COUNTY']

columna = columna.str.title()
columna2 = columna2.str.title()
columna3 = columna3.str.title()
columna4 = 'United States'

csv['NAME'] = columna
csv['CITY'] = columna2
csv['COUNTY'] = columna3
csv['COUNTRY'] = columna4


csv.to_csv(
    'HandsOn/Group08/csv2/us-colleges-and-universities-modified.csv', index=False)
