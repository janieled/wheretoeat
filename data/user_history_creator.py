import csv
import random
from datetime import datetime, timedelta

# File path
file_path = 'C:/Users/ljman/Documents/GitHub/wheretoeat/data/user_history.csv'

# Generate 100 new rows
new_rows = []
ratings = ['yes'] * 30 + ['None'] * 30 + ['no'] * 30 + ['meh'] * 10
user_id_start = 9  # Start user_id from 9 since 8 is the last in the current file

for i in range(100):
    user_id = user_id_start + i
    restaurant_id = random.randint(1, 20)  # Assuming 20 restaurants
    visit_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 364))
    visit_date = visit_date.strftime('%Y-%m-%d')
    rating = random.choice(ratings)
    new_rows.append([user_id, restaurant_id, visit_date, rating])

# Write to the CSV file
with open(file_path, 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(new_rows)

print("100 new rows added successfully.")