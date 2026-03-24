import pandas as pd
import sqlite3
import time
import os

print("🚀 NEW STREAM STARTED")

# DB path
db_path = os.path.join(os.getcwd(), "ecommerce.db")
print("DB will be created at:", db_path)

# Connect DB
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    price REAL,
    category TEXT,
    profit REAL
)
""")

conn.commit()

# Load CSV
df = pd.read_csv("data/ecommerce.csv", sep="\t")

# remove hidden spaces
df.columns = df.columns.str.strip()

# check columns
print("Columns:", df.columns)

print("✅ CSV Loaded")

# Insert data
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO sales (product, price, category, profit) VALUES (?, ?, ?, ?)",
        (row['Product'], row['Sales'], row['Category'], row['Profit'])
    )
    conn.commit()

    print("Inserted:", row['Product'])
    time.sleep(1)

conn.close()

print("✅ DONE")