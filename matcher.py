import re
import pandas as pd

filename = "Preprocessed02012021.xlsx"

df = pd.read_excel(filename)

df["Price"] = df["Price"].apply(lambda item: re.search(r"\d{4,9}", str(item))[0])

df["Bedrooms"] = df["Bedrooms"].apply(lambda item:re.search(r"\d{1,2}", str(item))[0])
df["Bathrooms"] = df["Bathrooms"].apply(lambda item:re.search(r"\d{0,2}", str(item))[0])
df["Living Space"] = df["Living Space"].apply(lambda item:re.search(r"\d{0,4}", str(item))[0])
df["Land Area"] = df["Land Area"].apply(lambda item:re.search(r"\d{0,4}", str(item))[0])

df.to_excel(str("Finaldata.xlsx"))