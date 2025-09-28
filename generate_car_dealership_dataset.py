"""
generate_car_dealership_dataset.py
This script generates a sample dataset for a car dealership and populates it into Azure Table Storage and Azure Blob Storage.
It is designed for educational and lab purposes, demonstrating how to work with Azure Storage services using Python.
Features:
---------
- Randomly generates car inventory data, including make, model, year, price, color, and mileage.
- Uploads a sample car image for each car entry to Azure Blob Storage.
- Stores car metadata in Azure Table Storage, including a reference to the image blob path.
- Automatically creates the required Azure Table and Blob Container if they do not exist.
How it works:
-------------
1. Connects to Azure Table Storage and Blob Storage using provided credentials.
2. Defines pools of car makes, models, categories, and colors for random data generation.
3. For each car entry:
  - Randomly selects category, make, model, year, price, color, and mileage.
  - Uploads a local image file (e.g., 'car.png') to Blob Storage, naming it according to the car's RowKey.
  - Inserts or updates the car entity in Azure Table Storage, including a reference to the image's blob path.
4. Prints progress and summary information to the console.
Configuration:
--------------
- Set the `username` variable to your own identifier (letters and numbers only).
- Update Azure Storage credentials (`account_name` and `account_key`) as needed.
- Place a sample image file (e.g., 'car.png') in the script's directory. One is provided for convenience.
Requirements:
-------------
- Python 3.x
- azure-data-tables
- azure-storage-blob
Intended Use:
-------------
- For students and instructors learning about Azure Storage, Python scripting, and data generation for cloud-based applications.
- Not intended for production use or with sensitive data.

"""
import random
from azure.data.tables import TableServiceClient, TableEntity
from azure.storage.blob import BlobServiceClient
 
# Input your username, with no special characters, just numbers and letters.
username= # "your_username"

# Replace with your Azure Storage credentials
account_name="account_name"
account_key="account_key"

# Table and container names
table_name = f"{username}CarInventory"
container_name = f"{username}cardealer"

# Local image path
local_image_path = "car.png"

# Connect to Azure Table Storage
connection_string="DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net".format(
  account_name=account_name,
  account_key=account_key
)
 
table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
table_client = table_service.get_table_client(table_name=table_name)
 
# Create table if it doesn’t exist
try:
  table_client.create_table()
  print(f"Table '{table_name}' created.")
except:
  print(f"Table '{table_name}' already exists.")

# Connect to Blob Storage
blob_service_client = BlobServiceClient(
  account_url=f"https://{account_name}.blob.core.windows.net",
  credential=account_key
)

# Create the container if it doesn't exist
container_client = blob_service_client.get_container_client(container_name)
try:
  container_client.create_container()
  print(f"Container '{container_name}' created.")
except Exception:
  print(f"Container '{container_name}' already exists.")
 
# --- Data Pools ---
makes_and_models = {
  "Toyota": ["Corolla", "Camry", "RAV4"],
  "Ford": ["Focus", "Fiesta", "Explorer"],
  "Honda": ["Civic", "Accord", "CR-V"],
  "Tesla": ["Model 3", "Model S", "Model Y"],
  "BMW": ["3 Series", "5 Series", "X3"],
  "Hyundai": ["Elantra", "Tucson", "Santa Fe"]
}
 
categories = {
  "Sedan": ["Toyota", "Ford", "Honda", "Hyundai"],
  "SUV": ["Toyota", "Ford", "Honda", "BMW", "Hyundai"],
  "Electric": ["Tesla"],
  "Luxury": ["BMW", "Tesla"]
}
 
colors = ["Red", "Black", "White", "Blue", "Silver", "Gray"]
 
def generate_car_entity(index):
  category = random.choice(list(categories.keys()))
  make = random.choice(categories[category])
  model = random.choice(makes_and_models[make])
  year = random.randint(2015, 2025)
  price = random.randint(15000, 60000)
  color = random.choice(colors)
  mileage = random.randint(10000, 120000)
  blob_path = f"{container_name}/CAR{index:03}.png" # You can use different images for each car later match this to actual blobs
 
  entity = TableEntity()
  entity["PartitionKey"] = category
  entity["RowKey"] = f"CAR{index:03}"
  entity["make"] = make
  entity["model"] = model
  entity["year"] = year
  entity["price"] = price
  entity["color"] = color
  entity["mileage"] = mileage
  entity["blob_path"] = blob_path
  return entity
 
# --- Generate and upload ---
NUM_CARS = 20 # Change to any number
 
for i in range(1, NUM_CARS + 1):
  car = generate_car_entity(i)

  # Upload the image
  blob_name = f"{car['RowKey']}.png"
  with open(local_image_path, "rb") as data:
    container_client.upload_blob(name=blob_name, data=data, overwrite=True)
    print(f"Uploaded {blob_name} to blob storage.")
  table_client.upsert_entity(car)
  print(f"Added: {car['RowKey']} - {car['make']} {car['model']} (${car['price']})")
print(f"\n✅ Successfully populated Azure Table with {NUM_CARS} car entries.")