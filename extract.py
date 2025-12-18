import pandas as pd
import sqlite3
import os

STAGING_DB = "staging.db"

def load_folder_to_staging(folder_path, table_prefix):
    conn = sqlite3.connect(STAGING_DB)
    
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            csv_path = os.path.join(folder_path, file)
            df = pd.read_csv(csv_path)
            table_name = f"{table_prefix}_{os.path.splitext(file)[0]}"
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"Loaded {csv_path} → {table_name}")
    
    conn.close()

if __name__ == "__main__":
    load_folder_to_staging("data/japan_store", "japan")
    load_folder_to_staging("data/myanmar_store", "myanmar")