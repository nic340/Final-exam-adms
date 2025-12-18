import pandas as pd
import sqlite3
import os

STAGING_DB = "staging.db"

def load_csv_to_staging(csv_path, table_name):
    """Load a CSV file into SQLite staging database"""
    conn = sqlite3.connect(STAGING_DB)
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print(f"{table_name} loaded into staging successfully.")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    load_csv_to_staging("data/japan_store.csv", "japan_store_staging")
    load_csv_to_staging("data/myanmar_store.csv", "myanmar_store_staging")