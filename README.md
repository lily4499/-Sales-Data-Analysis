

## 1. Dataset Selection

We'll use **Sample Sales Data** from Kaggle – it contains order info, sales, customer, and shipping data ideal for monthly trends .

---

## 2. Project Setup (CLI)

```bash
# 1. Create a project directory
mkdir sales-trends && cd sales-trends

# 2. Initialize a Python environment
python3 -m venv venv && source venv/bin/activate
pip install pandas matplotlib seaborn jupyter

# 3. Download the CSV (manually from Kaggle UI or use Kaggle CLI)
kaggle datasets download kyanyoga/sample-sales-data -f SampleSalesData.csv
unzip sample-sales-data.zip
```

---

## 3. Folder Structure

```
sales-trends/
├── data/
│   └── SampleSalesData.csv
├── notebooks/
│   └── EDA.ipynb
├── src/
│   ├── clean_data.py
│   └── analyze.py
└── requirements.txt
```

`requirements.txt` captures your dependencies (pandas, seaborn, matplotlib).

---

## 4. Data Cleaning (`src/clean_data.py`)

```python
import pandas as pd

def clean_sales(in_path, out_path):
    df = pd.read_csv(in_path, parse_dates=['Order Date'])
    df = df.drop_duplicates(subset='Order ID')
    df = df[df['Order Date'].notna()]
    df['YearMonth'] = df['Order Date'].dt.to_period('M')
    df['Sales'] = df['Quantity Ordered'] * df['Price Each']
    df.to_csv(out_path, index=False)

if __name__ == '__main__':
    clean_sales('../data/SampleSalesData.csv', '../data/cleaned_sales.csv')
```

**CLI usage:**

```bash
python src/clean_data.py
```

---

## 5. Exploratory Analysis (`src/analyze.py`)

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze(in_path):
    df = pd.read_csv(in_path, parse_dates=['Order Date'])
    monthly_sales = df.groupby('YearMonth')['Sales'].sum().reset_index()
    monthly_sales['YearMonth'] = monthly_sales['YearMonth'].dt.to_timestamp()
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_sales, x='YearMonth', y='Sales', marker='o')
    plt.title('Monthly Sales Trend')
    plt.xlabel('Month')
    plt.ylabel('Total Sales ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('monthly_sales.png')
    plt.show()
    
    top_products = (df.groupby('Product')['Sales']
                    .sum().sort_values(ascending=False).head(10))
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_products.values, y=top_products.index)
    plt.title('Top 10 Products (by Sales)')
    plt.xlabel('Total Sales ($)')
    plt.tight_layout()
    plt.savefig('top_products.png')
    plt.show()
    
if __name__ == '__main__':
    analyze('../data/cleaned_sales.csv')
```

**CLI usage:**

```bash
python src/analyze.py
```

---

## 6. Statistical Analysis (Discount vs. Volume)

Enhance cleaning to include discount:

```python
df_clean = df.dropna(subset=['Discount %'])
corr = df_clean['Discount %'].corr(df_clean['Quantity Ordered'])
print(f"Correlation between discount and volume: {corr:.2f}")
```

Add this snippet at the end of `analyze.py`, interpret results (e.g. positive correlation suggests discounts drive volume).

---

## 7. Jupyter Notebook (`notebooks/EDA.ipynb`)

Replicate the above steps interactively:

* Data loading & inspection
* Cleaning checks
* Visualizations inline
* Discount-volume scatter plot + correlation value

---

## 8. Recommendations

* Increase stock/inventory **Q4** for the **Top 3 products** based on October–December trends.
* Consider **more aggressive discounts** if correlation shows they uplift sales volume significantly.
* Generate a monthly dashboard from the saved `monthly_sales.png` and `top_products.png`.

---

## 9. (Optional) Automation

Using Excel: import the cleaned CSV into Power Query, build charts, and set up monthly data refresh via “Refresh All”.

Or script automations (e.g., cron job):

```bash
0 0 1 * * cd /path/sales-trends && \
git pull && \
source venv/bin/activate && \
python src/clean_data.py && \
python src/analyze.py
```

---

## Files Overview

* **data/SampleSalesData.csv** — source raw data
* **data/cleaned\_sales.csv** — processed data
* **src/clean\_data.py** — cleaning logic
* **src/analyze.py** — EDA & analysis logic (line/bar charts + discount correlation)
* **notebooks/EDA.ipynb** — interactive exploration + plots + interpretations

---

This project pipeline shows:

1. **Problem definition** – monthly sales trends + top products.
2. **Data ingestion** via Kaggle CSV.
3. **Cleaning** duplicates, missing dates.
4. **EDA visualizations**: trend lines + bar charts.
5. **Statistical insight**: discount vs. volume correlation.
6. **Recommendations** for inventory and discounting.
7. **Reproducibility**: reusable scripts & clear folder structure.

You can clone this structure, run the scripts, and you'll have a self‑contained sales‑trends analysis. Want to dive deeper (e.g., segmentation, seasonality decomposition)? I can show how.
