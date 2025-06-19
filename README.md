`https://lily4499.github.io/Sales-Data-Analysis/sales_analysis.html`

---

**kaggle CLI tool**
```
pip install kaggle

Go to Kaggle > My Account
Scroll down to API → Click Create New API Token → it will download a file called kaggle.json
Move this file to:
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

kaggle datasets list -s sales

```



# 🎯 Sales Data Analysis

👉 *Business Question:* **What are the monthly sales trends for our products?**

---

# 1️⃣ Define Problem

**Purpose:**

* Identify product trends over time
* Understand which products sell well
* Help business stock inventory better for Q4

---

# 2️⃣ Full Project Setup

### 🗂️ Directory Structure:

```text
sales-data-analysis/
├── data/
│   └── sample_sales_data.csv
├── notebooks/
│   └── sales_analysis.ipynb
├── scripts/
│   └── clean_and_plot.py
├── output/
│   ├── monthly_sales.png
│   ├── top_products.png
│   └── cleaned_sales_data.csv
├── requirements.txt
└── README.md
```

---

# 3️⃣ CLI — Full Setup from Scratch

### a) Create Project Directory:

```bash
# Step 1: Create project folder
mkdir sales-data-analysis
cd sales-data-analysis

# Step 2: Create folders
mkdir data notebooks scripts output

# Step 3: Create virtual environment
python3 -m venv venv

# Step 4: Activate virtual environment
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Step 5: Create requirements.txt
echo "pandas==2.2.2
matplotlib==3.8.4
seaborn==0.13.2
jupyter==1.0.0" > requirements.txt

# Step 6: Install dependencies
pip install -r requirements.txt
```

---

# 4️⃣ Get the Data

### a) Download from Kaggle:

👉 [Kaggle: Sample Sales Data](https://www.kaggle.com/datasets/kyanyoga/sample-sales-data)

### b) Save CSV:

```bash
# Move CSV into data/
mv ~/Downloads/sample_sales_data.csv data/sample_sales_data.csv
```

---

# 5️⃣ Clean Data — Handle Missing Dates & Duplicates

### Purpose:

* Clean the raw data
* Prepare "YearMonth" for trends
* Save cleaned data

### CLI:

```bash
# Create script file
touch scripts/clean_and_plot.py
```

### File: `scripts/clean_and_plot.py`

```python
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
```

---

# 6️⃣ Explore Data

### Purpose:

* See **monthly trends**
* See **top 10 products**

### Extend `scripts/clean_and_plot.py`:

```python
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
```

---

# 7️⃣ Statistical Analysis — Correlation

### Purpose:

* See if discounts increase quantity ordered
* Dataset doesn’t have discounts — **simulate**:

```python
# Simulate discount %
df['discount_percent'] = 100 - (df['PRICEEACH'] / df['MSRP'] * 100)

# Correlation between discount % and quantity
correlation = df['discount_percent'].corr(df['QUANTITYORDERED'])
print(f"Correlation between discount % and quantity ordered: {correlation:.2f}")
```

---

# 8️⃣ No model needed — Descriptive

**Just analysis** — no ML required

* Trends
* Top products
* Correlation

---

# 9️⃣ Visualization

**Output Plots:**

```text
output/monthly_sales.png
output/top_products.png

cp output/monthly_sales.png /mnt/c/Users/lilia/Desktop/
cp output/top_products.png /mnt/c/Users/lilia/Desktop/


```

---

# 🔟 Recommendation

From monthly\_sales.png:

✅ Increase inventory of top products for Q4 (Oct-Dec)

---

# 🔁 Automation — Refresh Monthly

**Option 1: Manual CLI**

```bash
python scripts/clean_and_plot.py
```

**Option 2: Cronjob (Linux)**

```bash
# Run on 1st of every month at 8am
crontab -e

# Add line:
0 8 1 * * /path/to/venv/bin/python /path/to/sales-data-analysis/scripts/clean_and_plot.py
```

---

# Final 

```markdown
# 📊 Sales Data Analysis

## Business Question:
👉 What are the monthly sales trends for our products?

## Project Steps:
✅ Define problem  
✅ Get CSV from Kaggle  
✅ Clean data  
✅ Plot monthly sales  
✅ Plot top products  
✅ Correlation between discount & volume  
✅ Visualization with matplotlib  
✅ Recommendation: stock top sellers in Q4  
✅ Automation option (cronjob)

## Outputs:
- output/monthly_sales.png
- output/top_products.png
- output/cleaned_sales_data.csv
```

---

---


### 🎯 Business Question:

👉 What are the **monthly sales trends** for our products?

---

### ✅ Just "Descriptive Analysis":

| Item             | What you're doing?       | Tool                                       |
| ---------------- | ------------------------ | ------------------------------------------ |
| **Trends**       | Monthly sales trends     | line plot (matplotlib/seaborn)             |
| **Top products** | Which products sell most | bar plot (matplotlib/seaborn)              |
| **Correlation**  | Discount % vs Quantity   | correlation calculation (pandas `.corr()`) |

---

### ✅ Why "No ML required"?

* You are **not trying to predict the future**
* You are **not classifying or clustering** data
* You are simply **exploring existing data** and showing **visual trends**

---

### Summary:

| Action           | What it answers                            |
| ---------------- | ------------------------------------------ |
| **Trends**       | Do we sell more in certain months?         |
| **Top products** | Which products generate most revenue?      |
| **Correlation**  | Does discount % increase quantity ordered? |

---

### Result = Descriptive Insights (NO ML)

* Business can **increase stock** for top sellers in Q4
* Can decide whether discounts are helping or not
* All based on **plots and summary statistics** — no need for ML model.

---


