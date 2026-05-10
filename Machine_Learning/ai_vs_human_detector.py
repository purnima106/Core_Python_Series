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
