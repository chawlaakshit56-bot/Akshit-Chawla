import pandas as pd

# Load data
df = pd.read_csv("SALES DATA.csv")

# Standardize column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Data cleaning
df["quantity"] = df["quantity"].fillna(0)
df = df.dropna(subset=["date"])
df["date"] = pd.to_datetime(df["date"], dayfirst=True)
df = df.drop_duplicates()

# Feature engineering
df["total_sales"] = df["quantity"] * df["price"]
df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year

# Analysis
total_revenue = df["total_sales"].sum()
region_sales = df.groupby("region")["total_sales"].sum().reset_index()
product_sales = df.groupby("product")["total_sales"].sum().reset_index()
monthly_sales = df.groupby(["year", "month"])["total_sales"].sum().reset_index()

# Output
print("\nTotal Revenue:", total_revenue)
print("\nRegion-wise Sales:\n", region_sales)
print("\nProduct-wise Sales:\n", product_sales)

# Export for Excel & Power BI
df.to_csv("cleaned_sales_data.csv", index=False)
region_sales.to_csv("region_sales_summary.csv", index=False)
product_sales.to_csv("product_sales_summary.csv", index=False)
monthly_sales.to_csv("monthly_sales_summary.csv", index=False)

print("\n✅ Sales Data Analysis Project Completed Successfully!")

