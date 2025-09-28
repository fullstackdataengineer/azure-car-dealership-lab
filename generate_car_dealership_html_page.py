"""
generate_car_dealership_html_page.py
This script connects to Azure Table Storage and Azure Blob Storage to generate an HTML gallery page
showcasing a car dealership's inventory. It retrieves car metadata from an Azure Table, fetches
corresponding car images from Azure Blob Storage, and embeds the images directly into the HTML using
base64 encoding. The resulting HTML file displays each car's make, model, price, and image in a table.
Key Features:
- Connects to Azure Table Storage to query car inventory data.
- Connects to Azure Blob Storage to retrieve car images.
- Dynamically generates an HTML page with embedded images and car details.
- Uploads the generated HTML page to the Azure Blob Storage "$web" container for static website hosting.
Usage:
- Set the `username`, `account_name`, and `account_key` variables with your Azure credentials.
- Ensure that the Azure Table contains car entities with fields: 'make', 'model', 'price', and 'blob_path'.
- Ensure that the Blob Storage contains the referenced images in the specified containers.
- Run the script to generate 'index.html' and upload it as '<username>_index.html' to the '$web' container.
Dependencies:
- azure-data-tables
- azure-storage-blob
- base64
- os
Note:
- The script assumes that each car entity in the table has a 'blob_path' field in the format 'container/blob_name'.
- The '$web' container is used for static website hosting on Azure Blob Storage.
"""
from azure.data.tables import TableServiceClient
from azure.storage.blob import BlobServiceClient, ContentSettings
import base64
import os

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
 
# Connect to Blob
blob_service = BlobServiceClient(
    account_url=f"https://{account_name}.blob.core.windows.net",
    credential=account_key
)
 
# Query Table
# cars = table_client.query_entities("PartitionKey eq 'Sedan'")

cars = table_client.list_entities()
total_cars = len(list(table_client.list_entities()))

# Generate HTML
html_filename = "index.html"
with open(html_filename, "w") as f:
    f.write(f"<html><head><title>{username.title()}'s Car Dealership</title></head><body>")
    f.write(f"<h1>{username.title()}'s Car Dealership</h1>\n")
    f.write(f"<p>Total cars in inventory: {total_cars}</p>\n")
    f.write("<table border='1' cellpadding='10'>")
    f.write("<tr><th>Car</th><th>Image</th></tr>\n")


    for car in cars:
        blob_path = car["blob_path"] # e.g., "container/car001.jpg"
        container, blob_name = blob_path.split("/", 1)


        # Read blob as bytes
        blob_client = blob_service.get_blob_client(container=container, blob=blob_name)
        blob_bytes = blob_client.download_blob().readall()


        # Convert to base64 for inline embedding
        img_b64 = base64.b64encode(blob_bytes).decode("utf-8")
        ext = os.path.splitext(blob_name)[1][1:] # jpg, png, etc.


        f.write("<tr>")
        f.write(f"<td>{car['make']} {car['model']}<br>Price: ${car['price']}</td>")
        f.write(f"<td><img src='data:image/{ext};base64,{img_b64}' width='300'></td>")
        f.write("</tr>\n")


    f.write("</table></body></html>")


print(f"✅ {html_filename} created. Preview it locally or upload to Azure.")

# Now, push index.html to $web container for static website hosting as {username}_index.html
web_container = "$web"
web_blob_client = blob_service.get_blob_client(container=web_container, blob=f"{username}_index.html")

# Create $web container if it doesn't exist
container_client = blob_service.get_container_client(web_container)
try:
    container_client.create_container()
    print(f"Container '{web_container}' created.")
except Exception:
    print(f"Container '{web_container}' already exists.")

with open("index.html", "rb") as data:
    web_blob_client.upload_blob(data, overwrite=True, content_settings=ContentSettings(content_type="text/html"))