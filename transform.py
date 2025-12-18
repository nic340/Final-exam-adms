import sqlite3
import pandas as pd

TRANSFORM_DB = "transformed.db"
EXCHANGE_RATE_USD_TO_JPY = 150  # Example conversion rate

def clean_and_transform(table_name, conn):
    """Read from staging, clean, and standardize data"""
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    
    # 1. Strip whitespace from column names
    df.columns = df.columns.str.strip()
    
    # 2. Strip whitespace inside string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
    
    # 3. Replace empty strings with NaN
    df.replace("", pd.NA, inplace=True)
    
    # 4. Drop duplicate rows
    df.drop_duplicates(inplace=True)
    
    # 5. Standardize prices
    if "price" in df.columns:
        if "japan" in table_name:
            df["price_usd"] = df["price"] / EXCHANGE_RATE_USD_TO_JPY
        else:
            df["price_usd"] = df["price"]  # already in USD
    
    return df

def save_transformed(df, table_name):
    conn = sqlite3.connect(TRANSFORM_DB)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"{table_name} saved to transformation area.")

if __name__ == "__main__":
    staging_conn = sqlite3.connect("staging.db")
    japan_df = clean_and_transform("japan_store_staging", staging_conn)
    myanmar_df = clean_and_transform("myanmar_store_staging", staging_conn)
    staging_conn.close()
    
    save_transformed(japan_df, "japan_store_transformed")
    save_transformed(myanmar_df, "myanmar_store_transformed")
