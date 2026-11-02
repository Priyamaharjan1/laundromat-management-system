import json
import pandas as pd
import matplotlib.pyplot as plt

with open("practice_orders.json") as f:
    orders = json.load(f)

df = pd.DataFrame(orders)

print(df)
print("\nTotal revenue: $", round(df["total"].sum(), 2))

df["date"] = pd.to_datetime(df["date"])
df["day"] = df["date"].dt.date
df["weekday"] = df["date"].dt.day_name()

print("\nTop customers:")
print(df.groupby("customer_id")["total"].sum().sort_values(ascending=False))

print("\nRevenue per day:")
print(df.groupby("day")["total"].sum())

print("\nOrders per weekday:")
print(df["weekday"].value_counts())


top = df.groupby("customer_id")["total"].sum().sort_values(ascending=False)

top.plot(kind="bar")
plt.title("Top Customers")
plt.ylabel("Total spent ($)")
plt.tight_layout()
plt.savefig("top_customers.png")
plt.show()


daily = df.groupby("day")["total"].sum()

plt.figure(figsize=(12, 5))
plt.bar(range(len(daily)), daily.values)

plt.title("Revenue per Day")
plt.xlabel("Date")
plt.ylabel("Revenue ($)")

plt.xticks(
    range(0, len(daily), 7),
    [str(d) for d in daily.index[::7]],
    rotation=45,
    ha="right"
)

plt.tight_layout()
plt.savefig("daily_revenue.png")
plt.show()

