import sqlite3
import pandas as pd

PRESENTATION_DB = "presentation.db"

def generate_insights():
    conn = sqlite3.connect(PRESENTATION_DB)
    df = pd.read_sql("SELECT * FROM big_table", conn)
    conn.close()

    # 1. Total items
    total_items = len(df)
    
    # 2. Average price USD
    avg_price = df['price_usd'].mean()
    
    # 3. Most expensive item
    most_expensive_item = df.loc[df['price_usd'].idxmax()]['product_name']
    
    # 4. Items per store (using 'city' column)
    items_per_store = df['city'].value_counts()
    
    # 5. Average price per category
    avg_price_category = df.groupby('category')['price_usd'].mean()

    # Print insights
    print("===== Analytics Insights =====")
    print(f"1. Total items: {total_items}")
    print(f"2. Average price USD: {avg_price:.2f}")
    print(f"3. Most expensive item: {most_expensive_item}")
    print("4. Items per store:")
    print(items_per_store)
    print("5. Average price per category:")
    print(avg_price_category)

    # Save insights to CSV
    insights_df = pd.DataFrame({
        "Insight": [
            "Total items",
            "Average price USD",
            "Most expensive item"
        ],
        "Value": [
            total_items,
            round(avg_price,2),
            most_expensive_item
        ]
    })
    insights_df.to_csv("insights_summary.csv", index=False)
    print("\nInsights saved to 'insights_summary.csv'")

if __name__ == "__main__":
    generate_insights()