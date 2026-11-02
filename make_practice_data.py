import json
import random
from datetime import datetime, timedelta

random.seed(42)

TAXRATE = 0.06
COSTLAB = 0.50
customers = ["maha", "mahaok", "kamsp", "abcdde", "Bajra1234", "Shrestha0099"]

orders = []
start = datetime(2026, 8, 1)

for day_number in range(60):
    day = start + timedelta(days=day_number)

    if day.weekday() >= 5:
        how_many = random.randint(8, 14)
    else:
        how_many = random.randint(2, 6)

    for i in range(how_many):
        when = day.replace(hour=random.randint(8, 20), minute=random.randint(0, 59))
        lbs = round(random.uniform(2, 12), 1)
        subtotal = lbs * COSTLAB
        taxes = subtotal * TAXRATE
        orders.append({
            "date": when.strftime("%Y-%m-%d %H:%M"),
            "customer_id": random.choice(customers),
            "pounds": lbs,
            "subtotal": round(subtotal, 2),
            "taxes": round(taxes, 2),
            "total": round(subtotal + taxes, 2),
        })

with open("practice_orders.json", "w") as f:
    json.dump(orders, f, indent=2)

print("Made", len(orders), "practice orders")