"""
azure_table_queries.py
This script demonstrates how to query and interact with Azure Table Storage using the Azure SDK for Python.
It provides a variety of example queries to retrieve and process car inventory data stored in an Azure Table.
Purpose:
    - To showcase different querying techniques for Azure Table Storage, including filtering, combining conditions,
      partial matches, sorting, and counting entities.
    - To serve as an educational resource for students or developers learning how to use Azure Table Storage in Python.
Main Features:
    1. Query all cars in a specific category (PartitionKey).
    2. Retrieve cars below a certain price threshold.
    3. Filter cars by color.
    4. Find cars from a specific year.
    5. Combine multiple conditions using AND logic.
    6. Combine multiple conditions using OR logic.
    7. Perform partial matches (e.g., models starting with a specific letter).
    8. Query cars within a price range.
    9. Sort query results manually by price.
    10. Count the total number of cars in the inventory.
Requirements:
    - Azure Table Storage account credentials (account name and key).
    - The Azure SDK for Python (`azure-data-tables`).
Configuration:
- Set the `username` variable to your own identifier (letters and numbers only).
- Update Azure Storage credentials (`account_name` and `account_key`) as needed.
Note:
    - The queries assume a table schema with fields such as PartitionKey, make, model, price, color, and year.
"""

from azure.data.tables import TableServiceClient
 
# Input your username, with no special characters, just numbers and letters.
username= # "your_username"

# Replace with your Azure Storage credentials
account_name="account_name"
account_key="account_key"

table_name=f"{username}CarInventory"
 
# Connect to Table
connection_string="DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net".format(
  account_name=account_name,
  account_key=account_key
)
 
table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
table_client = table_service.get_table_client(table_name=table_name)


print("1. 🚗 All Cars in a Category (PartitionKey)")
# Query all cars in the 'SUV' category
cars = table_client.query_entities("PartitionKey eq 'SUV'")

for c in cars:
    print(f"{c['PartitionKey']} {c['make']} {c['model']} - ${c['price']}")

print("2. 💰 Cars Below a Price Threshold")
# Query cars priced below $20,000
cars = table_client.query_entities("price lt 20000")

for c in cars:
    print(f"{c['make']} {c['model']} - ${c['price']}")

print("3. 🎨 Cars by Color")
# Query cars that are Red
cars = table_client.query_entities("color eq 'Red'")
for c in cars:
    print(f"{c['make']} {c['model']} - ${c['price']} - Color: {c['color']}")

print("4. 📆 Cars from a Specific Year")
# Query cars from the year 2020
cars = table_client.query_entities("year eq 2020")
for c in cars:
    print(f"{c['make']} {c['model']} - ${c['price']} - Year: {c['year']}")

print("5. 🧠 Combine AND Conditions")
# Query cars that are Sedans and priced below $18,000
cars = table_client.query_entities("PartitionKey eq 'Sedan' and price lt 18000")
for c in cars:
    print(f"{c['make']} {c['model']} - ${c['price']} - Category: {c['PartitionKey']}")

print("6. 🧪 Combine OR Conditions")
# Query cars that are either Toyota or Honda
cars = table_client.query_entities("make eq 'Toyota' or make eq 'Honda'")
for c in cars:
    print(f"{c['make']} {c['model']} - ${c['price']}")

print("7. 🔍 Partial Match (Starts With)")
# Get all Toyota cars and filter manually by model prefix
cars = table_client.query_entities("make eq 'Toyota'")
filtered = [car for car in cars if car['model'].startswith("C")]

for c in filtered:
    print(f"{c['make']} {c['model']} - ${c['price']}")

print("8. 📈 Price Range Query")  
# Get cars priced between $15,000 and $30,000
cars = table_client.query_entities("price ge 15000 and price le 30000")
for c in cars:
    print(f"{c['make']} {c['model']} - ${c['price']}")

print("9. 🧮 Sort by Price (Manually)")
# Get all SUV cars and sort by price
cars = list(table_client.query_entities("PartitionKey eq 'SUV'"))
sorted_cars = sorted(cars, key=lambda x: x['price'])

for c in sorted_cars:
    print(f"{c['make']} {c['model']} - ${c['price']}")

print("10. 🏷️ Count the total number of cars in the Table")
# Note: Azure Table Storage does not support COUNT queries directly.
# We retrieve all entities and count them in Python.
cars = list(table_client.list_entities())
print(f"Total cars in inventory: {len(cars)}")


