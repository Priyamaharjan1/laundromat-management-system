import json
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

with open("practice_orders.json") as f:
    orders = json.load(f)

df = pd.DataFrame(orders)
df["date"] = pd.to_datetime(df["date"])
df["day"] = df["date"].dt.date
df["weekday"] = df["date"].dt.day_name()

per_day = df.groupby(["day", "weekday"]).size().reset_index(name="orders")

week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
average = per_day.groupby("weekday")["orders"].mean().reindex(week).round(1)

print("Average orders per weekday (practice data):")
print(average)

busiest = average.idxmax()
print("\nPrediction: the busiest day is", busiest)

tomorrow = (datetime.now() + timedelta(days=1)).strftime("%A")
print("Expected orders tomorrow (" + tomorrow + "):", average[tomorrow])

average.plot(kind="bar")
plt.title("Average Orders per Weekday (practice data)")
plt.ylabel("Orders")
plt.tight_layout()
plt.savefig("busy_days.png")
plt.show()