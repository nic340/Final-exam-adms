import sqlite3
import pandas as pd

STAGING_DB = "staging.db"
TRANSFORM_DB = "transformed.db"
EXCHANGE_RATE_JPY_TO_USD = 150  # Example: 1 USD = 150 JPY

def clean_and_transform(df, store_prefix):
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Clean text columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
    
    # Replace empty strings with NaN
    df.replace("", pd.NA, inplace=True)
    
    # Drop duplicates
    df.drop_duplicates(inplace=True)
    
    # Standardize price
    if "price" in df.columns:
        if store_prefix == "japan":
            df["price_usd"] = df["price"] / EXCHANGE_RATE_JPY_TO_USD
        else:
            df["price_usd"] = df["price"]
    
    return df

def transform_all_tables():
    staging_conn = sqlite3.connect(STAGING_DB)
    transform_conn = sqlite3.connect(TRANSFORM_DB)
    
    # Get all tables from staging
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", staging_conn)
    
    for table in tables['name']:
        df = pd.read_sql(f"SELECT * FROM {table}", staging_conn)
        store_prefix = table.split("_")[0]  # first part of table name
        df_clean = clean_and_transform(df, store_prefix)
        df_clean.to_sql(f"{table}_transformed", transform_conn, if_exists='replace', index=False)
        print(f"Transformed {table} → {table}_transformed")
    
    staging_conn.close()
    transform_conn.close()

if __name__ == "__main__":
    transform_all_tables()