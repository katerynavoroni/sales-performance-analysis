import pandas as pd
import sqlite3

# 📁 ścieżka do bazy (utworzy się automatycznie)
conn = sqlite3.connect("../data/sales.db")

# 📥 wczytaj CSV
customers = pd.read_csv("../data/customers.csv")
products = pd.read_csv("../data/products.csv")
orders = pd.read_csv("../data/orders.csv")

# 📦 zapis do SQLite (TO TWORZY TABELE!)
customers.to_sql("customers", conn, if_exists="replace", index=False)
products.to_sql("products", conn, if_exists="replace", index=False)
orders.to_sql("orders", conn, if_exists="replace", index=False)

print("✅ Database created successfully!")

conn.close()