# 🚗 Azure Car Dealership Lab – Python + Azure Blob & Table Storage

This lab teaches you how to use **Azure Storage Accounts** from Python to build a cloud-based inventory system for a car dealership. You is crucial knowledge go support your Group Project.

You will:
- Upload car **images** to **Azure Blob Storage**
- Store car **metadata** (make, model, price, image path) in **Azure Table Storage**
- Generate a static **HTML page** that displays cars and their images
- Deploy the HTML as a **static website using Azure Blob Static Website Hosting**

## Background information  

An Azure Storage Account is a foundational cloud service that allows you to store different types of data. Think of it like a virtual drive in the cloud where you can store:
- Files and images (via Blob Storage)
- Structured table-like data (via Table Storage)
- Message queues, and more.

You access a storage account using:

- Account name
- Account key

These are like a username and password pair for cloud access.  

---

## 🧰 Prerequisites

✅ An [Azure Storage Account](https://portal.azure.com/) with:
- Storage Account Name
- Storage Account Key

✅ Python 3.10 or later

✅ GitHub Codespaces or local Python environment

---

## 📦 Project Structure

```
azure-car-dealership-lab/
├── generate_car_dealership_dataset.py       # Create synthetic car data + upload to Azure
├── generate_car_dealership_html_page.py     # Generate and deploy HTML inventory page
├── azure_table_queries.py                   # A tutorial to learn how to get Table Storage data
├── car.png                                  # For simplicity, we use the same car image to represent each car in stock
├── index.html                               # Auto-generated HTML file (for $web hosting)
└── README.md                                # You are here ✅
```

---

## 🛠️ Setup Steps

### 1. Clone the Repository (or copy the scripts)

```bash
git clone <your-repo-url>
cd azure-car-dealership-lab
```

### 2. Set Up a Python Virtual Environment

```bash
mkdir azure-car-dealership-lab
cd azure-car-dealership-lab
python3 -m venv azurenv
source azurenv/bin/activate  # or .venv\Scripts\activate on Windows
```

### 3. Install Required Libraries

```bash
pip install azure-data-tables azure-storage-blob
```

---

## 🔍 Azure Storage Concepts (Educational)

### 🔷 Blob Storage ("Binary Large Objects")
- Stores images, PDFs, videos, documents, etc. in containers
- In this lab, you store car **photos** in blob containers (this is not the same as a docker container, think of it as a bucket that stores different files)
- Later you display these in your HTML UI

### 📋 Table Storage
- A NoSQL key-value database
- Used for structured records (like a table row)
- You store:
  - `make`, `model`, `price`, `color`
  - `blob_path`: which links to the image in Blob Storage
- Entities require:
  - `PartitionKey` (like category — groups related entities for faster queries and scalability)
  - `RowKey` (unique ID within that PartitionKey — uniquely identifies an entity, e.g., CAR001)
> Together, `PartitionKey` and `RowKey` form the **composite primary key** for each entity, enabling efficient lookups and high scalability in Azure Table Storage.


---

## 🚀 Script Overview

### 🏗️ `generate_car_dealership_dataset.py`
- Connects to Azure Blob + Table
- Creates:
  - A container for car images
  - A table for car metadata
- Generates **synthetic car entries**
- Uploads car images to a blob container
- Stores car image paths and car metadata (make, color, price...) in the table

Run it with:
```bash
python generate_car_dealership_dataset.py
```

NOTE: You must set the values for username, account_name and account_key inside the script

### 🖼️ `generate_car_dealership_html_page.py`
- Reads the car inventory from Table Storage
- Retrieves and embeds images using Blob Storage
- Generates a complete `index.html`
- Uploads it to the `$web` container for **static website hosting**

Run it with:
```bash
python generate_car_dealership_html_page.py
```

NOTE: You must set the values for username, account_name and account_key inside the script

### 🔍 `azure_table_queries.py`
- Demonstrates how to **filter, search, and sort** data in Azure Table Storage using LINQ-style queries
- Covers examples such as:
- Cars by category (PartitionKey)
- Cars under a price threshold
- Filtering by color or year
- Combining conditions with `and` / `or`
- Manual filtering using `startswith`
- Sorting results by price


Run it with:
```bash
python azure_table_queries.py
```

This script is excellent for exploring your dataset, validating your inserts, and learning how to build powerful serverless filters for real applications.

NOTE: You must set the values for username, account_name and account_key inside the script

---

## 🌐 Hosting the Inventory Page on Azure

Azure lets you serve `index.html` from the special `$web` blob container.

✅ After running the second script (generate_car_dealership_html_page.py), access your static site here:

```
https://<your_account>.z6.web.core.windows.net/<your_username>_index.html
```

> Example: https://accountname.z6.web.core.windows.net/instructor_index.html

---

## ✅ Summary: What You Learned

| Skill                      | Technology               |
|---------------------------|--------------------------|
| Upload images to cloud    | Azure Blob Storage       |
| Store structured data     | Azure Table Storage      |
| Build static websites     | Azure Blob ($web)        |
| Base64 encode & embed     | Python + HTML            |
| Python Azure SDK usage    | `azure-storage-blob`, `azure-data-tables` |

---

## 🧠 Bonus Ideas

- Upload real car images
- Add filtering by price or make to the HTML generator
- Generate more advanced HTML or CSS styling
- Add separate pages for each car  in the HTML generator
- Integrate into your **group project backend**

---

## 📚 References & Further Reading

### 🔷 Azure Table Storage Concepts

#### 🔹 What is a Storage Account?
📘 [Overview of Azure Storage Accounts (Microsoft Docs)]  
https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview  
> Learn about the different types of data supported in Azure Storage (blobs, tables, queues, and files), and how they work under a single storage account.

#### 🔹 PartitionKey and RowKey Explained
🧱 [Azure Table Storage Design Guide – PartitionKey & RowKey Basics]  
https://learn.microsoft.com/en-us/azure/storage/tables/table-storage-design-for-query  
> Understand how Azure Table Storage scales using `PartitionKey` and `RowKey` as a composite primary key, and how to design your data model for efficient queries and inserts.

#### 🔹 LINQ-style Queries in Azure Data Tables (Python)
💻 [Querying Tables in Azure SDK for Python (filter syntax)]  
https://learn.microsoft.com/en-us/samples/azure/azure-sdk-for-python/tables-samples/ 
> Includes examples of how to write filters like `"PartitionKey eq 'Sedan'"`, `"price gt 20000"`, etc.

---

### 🗂️ Azure Blob Storage

#### 🔹 Blob Storage Basics
📘 [What is Azure Blob Storage?]  
https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-overview  
> High-level overview of blob types (block, append, page), containers, and use cases.

#### 🔹 Upload and Download Blobs with Python
💡 [Quickstart: Upload and Download a Blob using Python]  
https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python  
> Walkthrough with real code for interacting with blobs in Python, similar to your lab.

---

### 🧪 Base64 Embedding for HTML

#### 🔹 Base64 Image Embedding
🖼️ [Data URLs in HTML `<img>` tags (MDN Web Docs)]  
https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs  
> Shows how images can be embedded in HTML using `data:image/jpeg;base64,...` format—ideal for secure internal image rendering.

---

### 🧰 Azure SDK for Python Reference Docs

📘 [Azure Storage Blob – SDK Reference (Python)]  
https://learn.microsoft.com/en-us/python/api/overview/azure/storage-blob-readme

📘 [Azure Data Tables – SDK Reference (Python)]  
https://learn.microsoft.com/en-us/python/api/overview/azure/data-tables-readme

---

### 🌐 Azure Static Website Hosting in Blob Storage

📘 [Host a static website in Azure Storage (Microsoft Learn)]  
https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-static-website

> This guide explains how to use Azure Blob Storage to host a static website, including how to:
> - Enable the `$web` container
> - Upload `index.html` and other static assets
> - Access your static site via a public web URL
> - Understand routing, MIME types, and common errors (like file download vs render)

✅ Once enabled, your static site is available at:

---

Happy Cloud Coding! ☁️🚗
