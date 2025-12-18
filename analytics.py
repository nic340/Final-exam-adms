import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

PRESENTATION_DB = "presentation.db"

def generate_insights():
    conn = sqlite3.connect(PRESENTATION_DB)
    df = pd.read_sql("SELECT * FROM big_table", conn)
    conn.close()

    # Insights
    total_items = len(df)
    avg_price = df['price_usd'].mean()
    most_expensive_item = df.loc[df['price_usd'].idxmax()]['product_name']
    items_per_store = df['city'].value_counts()
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

    # Save summary CSV
    insights_df = pd.DataFrame({
        "Insight": ["Total items", "Average price USD", "Most expensive item"],
        "Value": [total_items, round(avg_price,2), most_expensive_item]
    })
    insights_df.to_csv("insights_summary.csv", index=False)
    print("\nInsights saved to 'insights_summary.csv'")

    # Visualizations
    plt.figure(figsize=(10,6))
    avg_price_category.sort_values().plot(kind='bar', color='skyblue')
    plt.title("Average Price per Category (USD)")
    plt.ylabel("Price USD")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("avg_price_category.png")
    plt.show()

    plt.figure(figsize=(6,6))
    items_per_store.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title("Items per Store")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("items_per_store.png")
    plt.show()

if __name__ == "__main__":
    generate_insights()