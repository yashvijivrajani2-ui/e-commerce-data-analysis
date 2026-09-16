import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file_path="C:/Users/Lenovo/OneDrive/Desktop/projects/E-commerce sales analytics/Online Retail.xlsx"

df=pd.read_excel(file_path)

# table info
print(df.head())
print(df.shape)
print(df.columns)
print(df.info())
print(df.dtypes)

# identify missing values
print(df.isnull())
print(df.isnull().sum())

# identify duplicate values
print(df.duplicated())
print(df.duplicated().sum())

# checking for unusual orders
# 1.quantity
print(df["Quantity"].describe())
print(df["Quantity"].sort_values().head(10))
print(df["Quantity"].sort_values(ascending=False).head(10))

# 2. unit price
print(df["UnitPrice"].describe())
print(df["UnitPrice"].sort_values().head(10))
print(df["UnitPrice"].sort_values(ascending=False).head(10))

# first 10 rows of negative quantity
print(df[df["Quantity"] < 0].head(10))
# first 20 rows of negative quantity invoice numbers
print(df[df["Quantity"] < 0]["InvoiceNo"].head(20))
# here, discovered that the negative quantites are associated with the invoice numbers starting with "C", which indicates that these are canceled orders.

# verfication of the discovered fact
print(df[(df["Quantity"] < 0)] )
print((df["InvoiceNo"].str.startswith("C")).value_counts())
# true for 9288 products and false for 3 products.

print(df[(df["Quantity"] < 0) & (~df["InvoiceNo"].astype(str).str.startswith("C"))][["InvoiceNo", "Quantity", "Description","UnitPrice"]].head(20))

print(((df["Quantity"] < 0) & (df["UnitPrice"] == 0) & (df["Description"].isnull())).sum())
# these are in total 862
# thus there are a total of 862 unusual data

# checking for nrgatives in unitprice column
print(df[df["UnitPrice"] < 0])
# only 2 records with negative unit price
# whose descriptions says "adjust bad debt" 
print(df.columns.to_list())

a=(df["CustomerID"].isnull().sum()/len(df))*100
print(a)
# apprximately 25% of the data has missing CustomerID values

b=(df["Description"].isnull().sum()/len(df))*100
print(b)
# 0.2683% precentage of the data has missing Description values

c=(862/len(df))*100
print(c)
# the 862 unusual data records represent approximately 0.16% of the total data
# there quantity is negative but there unit price is zero so they won't matter much during analysis as negative*0=0
# thus excluding these recordes

# there are 5268 duplicate rows
# identify their significance
d=(df.duplicated().sum()/len(df))*100
print(d)

clean_df=df.copy()
clean_df=clean_df.drop_duplicates()
print(clean_df.shape)
print(clean_df["InvoiceNo"].astype(str).str.startswith("C").sum())
print(clean_df[clean_df["InvoiceNo"].astype(str).str.startswith("C")]["Quantity"].describe())
print(clean_df.dtypes)

print("Unique countries in clean_df:")
print(clean_df["Country"].unique())

print(clean_df["Country"].value_counts().tail(10))
print(clean_df[clean_df["Country"].isin(["RSA", "European Community", "USA", "Unspecified", "Channel Islands"])]["Country"].value_counts())
print(clean_df["Country"].value_counts()["EIRE"])
clean_df["Country"] = clean_df["Country"].replace({
    "EIRE": "Ireland",
    "USA": "United States",
    "RSA": "South Africa"
})
print(clean_df["Country"].value_counts())

clean_df.to_csv("clean_ecommerce_data.csv", index=False)

import os

clean_df.to_csv("clean_ecommerce_data.csv", index=False)

print(os.path.abspath("clean_ecommerce_data.csv"))