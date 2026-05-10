import pandas as pd 
import numpy as np 
import re 

df = pd.read_csv(r"C:\Users\purni\Desktop\Core_Python_Series\Machine_Learning\ai_human_detection_v1.csv")
print("\n FIRST 5 ROWS OF DATASET:\n")
print(df.head())

print("\n\n INFORMATION OF DATASET:\n\n")
df.info()

print("\n\n SHAPE OF DATASET:\n\n")
print(df.shape)

print("\n DATA TYPES:\n")
print(df.dtypes)

#Phase 2-DATA INSPECTION + AUDITING

print("\n Missing Values: \n")
print(df.isnull().sum())

print("\n Duplicate Values: \n")
print(df.duplicated().sum())
duplicate_count = df.duplicated().sum()
print(f"\n Duplicate count is:{duplicate_count}")

print("\n Human VS AI Distribution: \n")
print(df['human_or_ai'].value_counts())

print("\n SAMPLE TEXT DATA:\n")

for i in range(5):
    print(f"\nROW {i+1}:")
    print(df['text'].iloc[i])

print("\n DATASET STATISTICS:\n")
print(df.describe(include='all'))

print("\n LANGUAGES PRESENT:\n")
print(df['language'].unique())

print("\n DOMAINS PRESENT:\n")
print(df['domain'].unique())




