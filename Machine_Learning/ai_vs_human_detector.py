import pandas as pd 
import numpy as np 
import re 

df = pd.read_csv(r"C:\Users\purni\Desktop\Core_Python_Series\Machine_Learning\ai_human_detection_v1.csv")
# print("\n FIRST 5 ROWS OF DATASET:\n")
# print(df.head())

# print("\n\n INFORMATION OF DATASET:\n\n")
# df.info()

# print("\n\n SHAPE OF DATASET:\n\n")
# print(df.shape)

# print("\n DATA TYPES:\n")
# print(df.dtypes)

#Phase 2-DATA INSPECTION + AUDITING

# print("\n Missing Values: \n")
# print(df.isnull().sum())

# print("\n Duplicate Values: \n")
# print(df.duplicated().sum())
# duplicate_count = df.duplicated().sum()
# print(f"\n Duplicate count is:{duplicate_count}")

# print("\n Human VS AI Distribution: \n")
# print(df['human_or_ai'].value_counts())

# print("\n SAMPLE TEXT DATA:\n")

# for i in range(5):
#     print(f"\nROW {i+1}:")
#     print(df['text'].iloc[i])

# print("\n DATASET STATISTICS:\n")
# print(df.describe(include='all'))

# print("\n LANGUAGES PRESENT:\n")
# print(df['language'].unique())

# print("\n DOMAINS PRESENT:\n")
# print(df['domain'].unique())

# Phase 3 - Data Cleaning + Preprocessing Pipeline

df = df.dropna(subset=['text'])

print("\n DATASET SHAPE AFTER REMOVING NULL TEXT:")
print(df.shape)

df = df.drop_duplicates()
print("\n DATASET SHAPE AFTER REMOVING DUPLICATES:")
print(df.shape)

error_patterns = [
    "404 client error",
    "400 client error",
    "api.groq.com",
    "not found for url"
]

def is_error_text(text):
    text = str(text).lower()

    for pattern in error_patterns:
        if pattern in text:
            return True
    return False

df = df[~df['text'].apply(is_error_text)]

print("\n DATASET SHAPE AFTER REMOVING ERROR ROWS:")
print(df.shape)

def clean_text(text):
    text = str(text)
    text = text.lower()

    text = re.sub(r'http\S+|www\S+', '', text)
    
    # remove extra spaces/newlines/tabs
    text = re.sub(r'\s+', ' ', text).strip()
    return text


df['clean_text'] = df['text'].apply(clean_text)

print("\n SAMPLE CLEANED TEXT:\n")

for i in range(5):
    print(f"\n ORIGINAL:")
    print(df['text'].iloc[i])
    
    print(f"\n CLEANED:")
    print(df['clean_text'].iloc[i])
    
    print("\n" + "="*50)







