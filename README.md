# Apple Store Product Price Scraper

This guide explains how the Python script for scraping Apple Store product prices works, how to run it, and the data structure of the output.

## Overview

This scraper fetches prices for various Apple products across multiple regions (USA, UAE, Australia, New Zealand, Germany). It aggregates prices and outputs a CSV file containing comparative pricing information.

## Requirements

- Python 3.x
- Libraries:
  - requests
  - beautifulsoup4
  - pandas

Install required libraries with:

`pip install requests beautifulsoup4 pandas`

## How the Script Works

1. **URLs & Products**: The script defines URLs for each Apple Store region and product type.

2. **Fetching Prices**:
    - Makes HTTP requests to each URL using a browser-like header.
    - Parses HTML content with BeautifulSoup.
    - Extracts JSON data embedded within the HTML.
    - Retrieves product names, specifications (SKU), and full prices.

3. **Data Aggregation**:
    - Initially gathers all product data from the USA store.
    - Matches products from other countries to the USA data by name.
    - Adds pricing data from other regions accordingly.

4. **Output Generation**:
    - Compiles collected data into a Pandas DataFrame.
    - Saves data to a CSV file (`apple_prices.csv`).

## Running the Script

Execute the script in your terminal or Python environment:

- Ensure your working directory contains the script.
- Run using:

`python your_script_name.py`

Replace `your_script_name.py` with the actual name of the Python file.

**Note**: The script has a built-in delay (`time.sleep(2)`) between requests to avoid rate limiting.

## Output File Structure

The CSV file (`apple_prices.csv`) includes:

- `ID`: Sequential identifier
- `Product Type`: General category (e.g., iPhone 16 Pro)
- `Product Name`: Exact product name as listed on the Apple website
- `Part Number`: SKU identifier
- Columns for each region: `USA`, `UAE`, `Australia`, `New Zealand`, `Germany` (prices listed in respective currencies)

## Handling Errors

The script logs errors in the console if:
- The JSON data isn't found on the page.
- A request fails due to network or HTTP errors.

Check the console output if data appears incomplete or unexpected.

## Customization

To add more regions or products, update the `base_urls` and `product_paths` dictionaries at the beginning of the script.

## Best Practices

- Avoid frequent requests to prevent IP blocking by Apple.
- Respect Apple's `robots.txt` guidelines and terms of use.
- Regularly verify and update URLs or JSON structure parsing logic to ensure data accuracy.

