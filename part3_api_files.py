import urllib.request
import urllib.error
import json
from datetime import datetime

# Error Logger

def log_error(context, error_type, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("error_log.txt", "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] ERROR in {context}: {error_type} — {message}\n")


# GET Request

def fetch_data(url, context="fetch_data"):
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)

    except urllib.error.URLError as e:
        print("Connection failed. Please check your internet.")
        log_error(context, "ConnectionError", str(e))
        return None

    except TimeoutError:
        print("Request timed out. Try again later.")
        log_error(context, "Timeout", "The request took too long.")
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error(context, "Exception", str(e))
        return None


# POST Request

def post_data(url, payload, context="post_data"):
    try:
        data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(request, timeout=5) as response:
            result = response.read().decode("utf-8")
            return json.loads(result)

    except urllib.error.URLError as e:
        print("Connection failed. Please check your internet.")
        log_error(context, "ConnectionError", str(e))
        return None

    except TimeoutError:
        print("Request timed out. Try again later.")
        log_error(context, "Timeout", "The request took too long.")
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error(context, "Exception", str(e))
        return None


# Task 1 — File Read & Write Basics

print("\nTASK 1 — File Read & Write Basics")
print("-" * 50)

notes_file = "python_notes.txt"

# Part A — Write
with open(notes_file, "w", encoding="utf-8") as file:
    file.write("Topic 1: Variables store data. Python is dynamically typed.\n")
    file.write("Topic 2: Lists are ordered and mutable.\n")
    file.write("Topic 3: Dictionaries store key-value pairs.\n")
    file.write("Topic 4: Loops automate repetitive tasks.\n")
    file.write("Topic 5: Exception handling prevents crashes.\n")

print("File written successfully.")

with open(notes_file, "a", encoding="utf-8") as file:
    file.write("Topic 6: Functions help organize code.\n")
    file.write("Topic 7: APIs help programs communicate with services.\n")

print("Lines appended.")

# Part B — Read
with open(notes_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

print("\nContents of python_notes.txt:")
for index, line in enumerate(lines, start=1):
    print(f"{index}. {line.strip()}")

print(f"\nTotal number of lines: {len(lines)}")

keyword = input("\nEnter a keyword to search in the file: ").strip().lower()
found = False

for line in lines:
    if keyword in line.lower():
        print(line.strip())
        found = True

if not found:
    print("No matching lines found for that keyword.")


# Task 3 — Exception Handling Part A

print("\nTASK 3A — Guarded Calculator")
print("-" * 50)

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print("safe_divide(10, 2)   =", safe_divide(10, 2))
print("safe_divide(10, 0)   =", safe_divide(10, 0))
print('safe_divide("ten", 2) =', safe_divide("ten", 2))


# Task 3 — Exception Handling Part B

print("\nTASK 3B — Guarded File Reader")
print("-" * 50)

def read_file_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    finally:
        print("File operation attempt complete.")

print("\nReading python_notes.txt:")
content1 = read_file_safe("python_notes.txt")
if content1 is not None:
    print(content1)

print("\nReading ghost_file.txt:")
content2 = read_file_safe("ghost_file.txt")
if content2 is not None:
    print(content2)


# Task 2 — API Integration

print("\nTASK 2 — API Integration")
print("-" * 50)

BASE_URL = "https://dummyjson.com/products"

# Step 1 — Fetch and Display Products
products = []

data = fetch_data(BASE_URL + "?limit=20", context="fetch_products")

if data and "products" in data:
    products = data["products"]

    print("\nID  | Title                          | Category      | Price    | Rating")
    print("-" * 75)
    for product in products:
        print(
            f"{str(product['id']):<3} | "
            f"{product['title'][:30]:<30} | "
            f"{product['category'][:12]:<12} | "
            f"${product['price']:<7} | "
            f"{product['rating']}"
        )
else:
    print("Could not fetch products.")

# Step 2 — Filter and Sort
print("\nFiltered products with rating >= 4.5, sorted by price descending:")
if products:
    filtered_products = [product for product in products if product["rating"] >= 4.5]
    filtered_products.sort(key=lambda item: item["price"], reverse=True)

    for product in filtered_products:
        print(f"{product['title']} | ${product['price']} | Rating: {product['rating']}")
else:
    print("No products available to filter.")

# Step 3 — Search by Category
print("\nLaptop products:")
laptop_data = fetch_data(BASE_URL + "/category/laptops", context="fetch_laptops")

if laptop_data and "products" in laptop_data:
    for laptop in laptop_data["products"]:
        print(f"{laptop['title']} - ${laptop['price']}")
else:
    print("Could not fetch laptop products.")

# Step 4 — POST Request
print("\nPOST response:")
new_product = {
    "title": "My Custom Product",
    "price": 999,
    "category": "electronics",
    "description": "A product I created via API"
}

post_response = post_data(BASE_URL + "/add", new_product, context="add_product")

if post_response:
    print(json.dumps(post_response, indent=4))
else:
    print("Could not complete POST request.")


# Task 3C and 3D — Robust API Calls + Input Validation Loop

print("\nTASK 3C & 3D — Product Lookup")
print("-" * 50)

while True:
    user_input = input("Enter a product ID to look up (1–100), or 'quit' to exit: ").strip()

    if user_input.lower() == "quit":
        break

    if not user_input.isdigit():
        print("Warning: Please enter a valid integer.")
        continue

    product_id = int(user_input)

    if product_id < 1 or product_id > 100:
        print("Warning: Product ID must be between 1 and 100.")
        continue

    product_url = f"{BASE_URL}/{product_id}"

    try:
        with urllib.request.urlopen(product_url, timeout=5) as response:
            if response.status == 200:
                product_data = json.loads(response.read().decode("utf-8"))
                print(f"Title: {product_data['title']}")
                print(f"Price: ${product_data['price']}")
            else:
                print("Unexpected response received.")
                log_error("lookup_product", "HTTPError", f"Unexpected status code {response.status}")

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("Product not found.")
            log_error("lookup_product", "HTTPError", f"404 Not Found for product ID {product_id}")
        else:
            print(f"HTTP Error: {e.code}")
            log_error("lookup_product", "HTTPError", str(e))

    except urllib.error.URLError as e:
        print("Connection failed. Please check your internet.")
        log_error("lookup_product", "ConnectionError", str(e))

    except TimeoutError:
        print("Request timed out. Try again later.")
        log_error("lookup_product", "Timeout", f"Timeout while requesting product ID {product_id}")

    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error("lookup_product", "Exception", str(e))


# Task 4 — Logging to File

print("\nTASK 4 — Logging to File")
print("-" * 50)

# Trigger 1: ConnectionError-like case
bad_url = "https://this-host-does-not-exist-xyz.com/api"
fetch_data(bad_url, context="test_connection")

# Trigger 2: HTTP 404 case
invalid_product_id = 999
invalid_url = f"{BASE_URL}/{invalid_product_id}"

try:
    with urllib.request.urlopen(invalid_url, timeout=5) as response:
        pass
except urllib.error.HTTPError as e:
    if e.code == 404:
        log_error("lookup_product", "HTTPError", f"404 Not Found for product ID {invalid_product_id}")
    else:
        log_error("lookup_product", "HTTPError", str(e))
except Exception as e:
    log_error("lookup_product", "Exception", str(e))

# Print full contents of error_log.txt
print("\nContents of error_log.txt:")
try:
    with open("error_log.txt", "r", encoding="utf-8") as file:
        print(file.read())
except FileNotFoundError:
    print("No log file found yet.")