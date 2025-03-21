import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time

# URLs for Apple Stores in different countries and product types
base_urls = {
    'USA': 'https://www.apple.com/shop/buy-',
    'UAE': 'https://www.apple.com/ae/shop/buy-',
    'Australia': 'https://www.apple.com/au/shop/buy-',
    'New Zealand': 'https://www.apple.com/nz/shop/buy-',
    'Germany': 'https://www.apple.com/de/shop/buy-'
}

product_paths = {
    'iPhone 16 Pro': 'iphone/iphone-16-pro',
    'iPhone 16': 'iphone/iphone-16',
    'iPhone 15': 'iphone/iphone-15',
    'iPhone 14': 'iphone/iphone-14',
    'iPhone SE': 'iphone/iphone-se',
    'iPad Pro': 'ipad/ipad-pro',
    'iPad Air': 'ipad/ipad-air',
    'iPad': 'ipad/ipad',
    'iPad Mini': 'ipad/ipad-mini',
    'AirPods 4': 'airpods/airpods-4',
    'AirPods Pro 2': 'airpods/airpods-pro-2',
    'AirPods Max': 'airpods/airpods-max'
}

apple_stores = {
    region: {product: f"{base}{product_paths[product]}" for product in product_paths}
    for region, base in base_urls.items()
}

# Function to extract prices from JSON embedded in the page's HTML
def get_all_prices(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        response.encoding = 'utf-8'  # Ensure correct encoding
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Locate the JSON data within a <script> tag
        json_script = soup.find('script', {'type': 'application/json', 'id': 'metrics'})
        
        if json_script:
            data = json.loads(json_script.string)
            product_info = data.get("data", {}).get("products", [])
            
            prices_list = []
            for product in product_info:
                if 'price' in product:
                    prices_list.append({
                        'product': product['name'],
                        'specs': product['sku'],
                        'price': f"${product['price']['fullPrice']}"
                    })
            return prices_list if prices_list else "No products found"
        else:
            return "No JSON data found"
    
    except requests.RequestException as e:
        return f"Error fetching prices: {e}"

# List to hold all products and prices
all_prices = []
product_map = {}

# First, get all products from the USA
print("\nFetching prices in USA...")
us_prices = []
for product_type, url in apple_stores['USA'].items():
    product_data = get_all_prices(url)
    
    if isinstance(product_data, list):
        for product in product_data:
            product_map[product['product']] = {
                'Product Type': product_type,
                'Product Name': product['product'],
                'Part Number': product['specs'],
                'USA': product['price']
            }
    else:
        print(f"  Error in USA for {product_type}: {product_data}")

# Now, loop through other markets to get prices
for country, products in apple_stores.items():
    if country != 'USA':
        print(f"\nFetching prices in {country}...")
        for product_type, url in products.items():
            product_data = get_all_prices(url)
            if isinstance(product_data, list):
                for product in product_data:
                    if product['product'] in product_map:
                        product_map[product['product']][country] = product['price']
                    else:
                        # If the product is not found in the USA, we add it to the map
                        product_map[product['product']] = {
                            'Product Type': product_type,
                            'Product Name': product['product'],
                            'Part Number': product['specs'],
                            country: product['price']
                        }
            else:
                print(f"  Error in {country} for {product_type}: {product_data}")

            time.sleep(2)  # Pause to avoid rate-limiting

# Convert the product map to a list for DataFrame creation
for product_data in product_map.values():
    all_prices.append({
        'ID': len(all_prices) + 1,
        **product_data
    })

# Create DataFrame and save to CSV
df = pd.DataFrame(all_prices)
df.to_csv('apple_prices.csv', index=False, encoding='utf-8')
print("\nData saved to 'apple_prices.csv'")
