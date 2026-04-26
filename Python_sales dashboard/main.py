import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect("../data/sales.db")

# 📊 QUERIES
q_category = """ SELECT p.category, SUM(o.quantity * p.price) AS total_sales
FROM orders o JOIN products p ON o.product_id = p.product_id
GROUP BY p.category ORDER BY total_sales DESC """

q_trend = """ SELECT strftime('%Y-%m', o.order_date) AS month,
SUM(o.quantity * p.price) AS monthly_sales
FROM orders o JOIN products p ON o.product_id = p.product_id
GROUP BY month ORDER BY month """

q_top = """ SELECT p.product_name,
SUM(o.quantity * p.price) AS total_sales
FROM orders o JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_name ORDER BY total_sales DESC LIMIT 5 """

q_city = """ SELECT c.city,
SUM(o.quantity * p.price) AS total_sales
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
GROUP BY c.city ORDER BY total_sales DESC """

q_rank = """ SELECT p.product_name,
SUM(o.quantity * p.price) AS total_sales
FROM orders o JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_name ORDER BY total_sales DESC """

q_aov = """
SELECT AVG(order_total) AS avg_order_value
FROM (
    SELECT o.order_id, SUM(o.quantity * p.price) AS order_total
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY o.order_id
)
"""
aov_df = pd.read_sql(q_aov, conn)


# 📥 LOAD DATA
category = pd.read_sql(q_category, conn)
trend = pd.read_sql(q_trend, conn)
top = pd.read_sql(q_top, conn)
city = pd.read_sql(q_city, conn)
rank = pd.read_sql(q_rank, conn)

# 🧠 KPI
total_revenue = category["total_sales"].sum()
best_category = category.iloc[0]["category"]
best_product = top.iloc[0]["product_name"]
avg_order_value = aov_df.iloc[0]["avg_order_value"]

# 📊 DASHBOARD
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("SALES ANALYTICS DASHBOARD", fontsize=18, fontweight="bold")
fig.patch.set_facecolor("#f5f5f5")
axes[0,0].set_facecolor("white")
for row in axes:
    for ax in row:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

# 📊 Category
axes[0, 0].bar(category["category"], category["total_sales"])
axes[0, 0].set_title("Sales by Category")
axes[0, 0].tick_params(axis="x", rotation=45)

# 📈 Trend
# axes[0, 1].plot(trend["month"], trend["monthly_sales"])
# axes[0, 1].set_title("Monthly Sales Trend")
# axes[0, 1].tick_params(axis="x", rotation=45)
trend["month"] = pd.to_datetime(trend["month"])
trend["forecast"] = trend["monthly_sales"].rolling(2).mean().bfill()
axes[0, 1].plot(trend["month"], trend["monthly_sales"], label="Actual")
axes[0, 1].plot(trend["month"], trend["forecast"], linestyle="--", label="Forecast")
axes[0, 1].legend()

# 🏆 Top products
axes[0, 2].bar(top["product_name"], top["total_sales"])
axes[0, 2].set_title("Top 5 Products")
axes[0, 2].tick_params(axis="x", rotation=45)

# 🌍 City
axes[1, 0].bar(city["city"], city["total_sales"], color="green")
axes[1, 0].set_title("Sales by City")
axes[1, 0].tick_params(axis="x", rotation=45)

# 🏆 Ranking
axes[1, 1].bar(rank["product_name"], rank["total_sales"], color="purple")
axes[1, 1].set_title("Product Ranking")
axes[1, 1].tick_params(axis="x", rotation=45)

# 📦 KPI + INSIGHTS
axes[1, 2].axis("off")
axes[1, 2].text(0.1, 0.8, f"Total Revenue: {total_revenue:.2f}", fontsize=14)
axes[1, 2].text(0.1, 0.6, f"Top Category: {best_category}", fontsize=14)
axes[1, 2].text(0.1, 0.4, f"Top Product: {best_product}", fontsize=14)
axes[1, 2].text(0.1, 0.7, f"Average Order Value: {avg_order_value:.2f}", fontsize=14)

axes[1, 2].text(
    0.1, 0.05,
    "Insights:\n"
    "- Electronics dominates revenue\n"
    "- Laptop is the top-selling product\n"
    "- London generates the highest sales\n"
    "- Sales dropped significantly in June",
    fontsize=11
)
axes[0, 1].set_title("Monthly Sales Trend & Forecast")
axes[0, 1].tick_params(axis="x", rotation=45)
axes[1, 1].axis("off")

plt.tight_layout()
plt.savefig("../output/sales_dashboard.png", dpi=300, bbox_inches="tight")
plt.show()