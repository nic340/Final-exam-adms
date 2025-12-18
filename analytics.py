import sqlite3
import pandas as pd

def generate_insights():
    conn = sqlite3.connect("presentation.db")
    df = pd.read_sql("SELECT * FROM big_table", conn)
    conn.close()
    
    print("===== Analytics Insights =====")
    print(f"1. Total items: {len(df)}")
    
    if "price_usd" in df.columns:
        print(f"2. Average price USD: {df['price_usd'].mean():.2f}")
        print(f"3. Most expensive item: {df.loc[df['price_usd'].idxmax()]['product_name']}")

    if "store_name" in df.columns:
        print(f"4. Items per store:\n{df['store_name'].value_counts()}")
    
    if "category" in df.columns:
        print(f"5. Average price per category:\n{df.groupby('category')['price_usd'].mean()}")

if __name__ == "__main__":
    generate_insights()