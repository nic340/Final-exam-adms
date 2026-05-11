import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# I-load ang credentials gikan sa .env file
load_dotenv()

# Kuhaon ang URL gikan sa .env
DATABASE_URL = os.getenv("DATABASE_URL")

def load_folder_to_staging(folder_path, table_prefix):
    """Load all CSV files in a folder to PostgreSQL Render DB"""
    
    # Kinahanglan i-fix ang URL format para sa SQLAlchemy (postgresql -> postgresql+psycopg2)
    # Importante ni para dili mag-error ang connection
    if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
        engine_url = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
    else:
        engine_url = DATABASE_URL

    # Paghimo og connection engine
    engine = create_engine(engine_url)
    
    print(f"--- 📂 Processing folder: {folder_path} ---")
    
    # Check kung nag-exist ba ang folder para dili mag-crash
    if not os.path.exists(folder_path):
        print(f"❌ Error: Folder '{folder_path}' dili makit-an!")
        return

    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            csv_path = os.path.join(folder_path, file)
            
            # Basahon ang CSV gamit ang Pandas
            df = pd.read_csv(csv_path)
            
            # Limpyohan ang table name (prefix + filename)
            table_name = f"{table_prefix}_{os.path.splitext(file)[0]}"
            
            # I-load sa PostgreSQL sa Render
            # if_exists='replace' para ma-refresh ang data kada run
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            
            print(f"✅ Loaded {file} → Render Table: {table_name}")
    
    print(f"--- Done processing {folder_path} ---\n")

if __name__ == "__main__":
    # Siguruha nga husto ang path sa imong folders sa VS Code
    load_folder_to_staging("data/japan_store", "japan")
    load_folder_to_staging("data/myanmar_store", "myanmar")