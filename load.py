import pandas as pd
import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def create_big_table():
    if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
        engine_url = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
    else:
        engine_url = DATABASE_URL

    engine = create_engine(engine_url)
    
    inspector = inspect(engine)
    all_tables = inspector.get_table_names()
    
    all_dfs = []
    
    print("--- 🏗️ Building BIG TABLE from PostgreSQL tables ---")
    
    for table_name in all_tables:
        if table_name != "big_table":
            df = pd.read_sql(f'SELECT * FROM "{table_name}"', engine)
            all_dfs.append(df)
            print(f"✅ Loaded {table_name} for BIG TABLE")
    
    if all_dfs:
        big_df = pd.concat(all_dfs, ignore_index=True)
        
        big_df.to_sql("big_table", engine, if_exists='replace', index=False)
        print("\n✨ SUCCESS: BIG TABLE created successfully in Render PostgreSQL!")
    else:
        print("❌ Error: No tables found in PostgreSQL to combine.")

if __name__ == "__main__":
    create_big_table()