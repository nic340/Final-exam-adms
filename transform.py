import pandas as pd
import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
EXCHANGE_RATE_JPY_TO_USD = 150

def clean_and_transform(df, store_prefix):
    df.columns = df.columns.str.strip()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
    df.replace("", pd.NA, inplace=True)
    df.drop_duplicates(inplace=True)
    if "price" in df.columns:
        if store_prefix == "japan":
            df["price_usd"] = df["price"] / EXCHANGE_RATE_JPY_TO_USD
        else:
            df["price_usd"] = df["price"]
    return df

def transform_all_tables():
    if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
        engine_url = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
    else:
        engine_url = DATABASE_URL

    engine = create_engine(engine_url)
    inspector = inspect(engine)
    all_tables = inspector.get_table_names()
    
    for table in all_tables:
        if not table.endswith("_transformed") and table != "big_table":
            df = pd.read_sql(f'SELECT * FROM "{table}"', engine)
            store_prefix = table.split("_")[0]
            df_clean = clean_and_transform(df, store_prefix)
            new_table_name = f"{table}_transformed"
            df_clean.to_sql(new_table_name, engine, if_exists='replace', index=False)
            print(f"✅ {new_table_name}")

if __name__ == "__main__":
    transform_all_tables()