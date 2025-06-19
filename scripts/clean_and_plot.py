import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load raw data
#df = pd.read_csv('data/sample_sales_data.csv', parse_dates=['ORDERDATE'])

# Load CSV with correct encoding!
df = pd.read_csv('data/sample_sales_data.csv', parse_dates=['ORDERDATE'], encoding='latin1')


# Clean: remove rows with missing dates
df = df.dropna(subset=['ORDERDATE'])

# Clean: drop duplicate rows
df = df.drop_duplicates()

# Create YearMonth column for trends
df['YearMonth'] = df['ORDERDATE'].dt.to_period('M')

# Save cleaned data
df.to_csv('output/cleaned_sales_data.csv', index=False)

print("✅ Cleaned data saved to output/cleaned_sales_data.csv")


# Monthly sales trend
monthly_sales = df.groupby('YearMonth')['SALES'].sum().reset_index()
monthly_sales['YearMonth'] = monthly_sales['YearMonth'].dt.to_timestamp()

plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_sales, x='YearMonth', y='SALES', marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('output/monthly_sales.png')
plt.close()

# Top 10 products by sales
top_products = df.groupby('PRODUCTCODE')['SALES'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_products.values, y=top_products.index)
plt.title('Top 10 Products by Sales')
plt.xlabel('Total Sales ($)')
plt.tight_layout()
plt.savefig('output/top_products.png')
plt.close()

print("✅ Plots saved in output/: monthly_sales.png, top_products.png")



# Simulate discount %
df['discount_percent'] = 100 - (df['PRICEEACH'] / df['MSRP'] * 100)

# Correlation between discount % and quantity
correlation = df['discount_percent'].corr(df['QUANTITYORDERED'])
print(f"Correlation between discount % and quantity ordered: {correlation:.2f}")

