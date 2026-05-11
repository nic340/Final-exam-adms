import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def load_folder_to_staging(folder_path, table_prefix):
    """Load all CSV files in a folder to PostgreSQL Render DB"""
    
    if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
        engine_url = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
    else:
        engine_url = DATABASE_URL

    engine = create_engine(engine_url)
    
    print(f"--- 📂 Processing folder: {folder_path} ---")
    
    if not os.path.exists(folder_path):
        print(f"❌ Error: Folder '{folder_path}' dili makit-an!")
        return

    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            csv_path = os.path.join(folder_path, file)
            
            df = pd.read_csv(csv_path)
            
            table_name = f"{table_prefix}_{os.path.splitext(file)[0]}"
            
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            
            print(f"✅ Loaded {file} → Render Table: {table_name}")
    
    print(f"--- Done processing {folder_path} ---\n")

if __name__ == "__main__":
    load_folder_to_staging("data/japan_store", "japan")
    load_folder_to_staging("data/myanmar_store", "myanmar")