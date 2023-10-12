import pandas as pd

path = "/home/alvaro/Desktop/OpenData&KG/ODKG/HandsOn/Group08/csv2/us-colleges-and-universities.csv"

df = pd.read_csv(path)

df = df.drop_duplicates(subset="IPEDSID", keep="last")

df.to_csv(path+"edited.csv")
