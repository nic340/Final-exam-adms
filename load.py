import sqlite3
import pandas as pd

PRESENTATION_DB = "presentation.db"

def create_big_table():
    conn = sqlite3.connect("transformed.db")
    japan_df = pd.read_sql("SELECT * FROM japan_store_transformed", conn)
    myanmar_df = pd.read_sql("SELECT * FROM myanmar_store_transformed", conn)
    conn.close()
    
    # Combine into one table
    big_df = pd.concat([japan_df, myanmar_df], ignore_index=True)
    
    # Save into presentation DB
    conn = sqlite3.connect(PRESENTATION_DB)
    big_df.to_sql("big_table", conn, if_exists="replace", index=False)
    conn.close()
    print("BIG TABLE created in presentation area.")

if __name__ == "__main__":
    create_big_table()