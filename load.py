import sqlite3
import pandas as pd

TRANSFORM_DB = "transformed.db"
PRESENTATION_DB = "presentation.db"

def create_big_table():
    transform_conn = sqlite3.connect(TRANSFORM_DB)
    presentation_conn = sqlite3.connect(PRESENTATION_DB)
    
    # Get all transformed tables
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", transform_conn)
    
    all_dfs = []
    for table in tables['name']:
        df = pd.read_sql(f"SELECT * FROM {table}", transform_conn)
        all_dfs.append(df)
        print(f"Loaded {table} for BIG TABLE")
    
    # Combine all dataframes
    big_df = pd.concat(all_dfs, ignore_index=True)
    
    # Save to presentation DB
    big_df.to_sql("big_table", presentation_conn, if_exists='replace', index=False)
    print("BIG TABLE created in presentation.db")
    
    transform_conn.close()
    presentation_conn.close()

if __name__ == "__main__":
    create_big_table()