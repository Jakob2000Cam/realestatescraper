import geopandas
import geopy
import pandas as pd

filename = "RealEstate02012021.xlsx"
locator = geopy.Nominatim(user_agent="myGeocoder")

df = pd.read_excel(filename)

print(df["Address"][:10])

df["Commune"] = df["Commune"].apply(lambda item: item[7:])

df["Latitude"] = ""
df["Longitude"] = ""

for ind in df.index:
    if df["Address"][ind] != 0:
        add = str(df["Address"][ind])+", "+str(df["Commune"][ind])+", Belgium"
        location = locator.geocode(add)
    elif df["Commune"][ind] == 0:
        df["Latitude"][ind] = 0
        df["Longitude"][ind] = 0
        continue
    else:
        location = locator.geocode(str(df["Commune"][ind])+", Belgium")
    if location != None:
        df["Latitude"][ind] = location.latitude
        df["Longitude"][ind] = location.longitude
    else:
        df["Latitude"][ind] = 0
        df["Longitude"][ind] = 0

print(df["Longitude"].head())
df.to_excel(str("Preprocessed.xlsx"))
#location = locator.geocode("Uccle, Belgium")

#print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))

