import pandas as pd

path = "/home/alvaro/Desktop/OpenData&KG/ODKG/HandsOn/Group08/csv2/us-colleges-and-universities.csv"

df = pd.read_csv(path)

duplicados = df['IPEDSID'].duplicated(keep=False)
print("Number of dups",len(df[duplicados]))

print("Old:", len(df))

df = df.drop_duplicates(subset="IPEDSID", keep="last")


print("New:",len(df))
df.to_csv(path[:-4]+"-edited.csv")
