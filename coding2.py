import requests
import sys
import logging

# Set up logging for easier debugging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Constant for the API URL base
API_URL_BASE = "https://dev.shopalyst.com/shopalyst-service/v1/products/"


def fetch_product_details(product_id: str) -> dict:
    """Fetch product details from Shopalyst API and return the raw data."""
    url = f"{API_URL_BASE}{product_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        product_data = response.json()  # Parse JSON data
        return product_data
    except requests.exceptions.RequestException as e:
        logging.error(
            f"Failed to fetch product data for product_id {product_id}: {e}")
        raise  # Reraise the exception for higher-level handling


def extract_sku_details_from_response(product_data: dict) -> list:
    """Extract SKU details from the product data response."""
    sku_details = []

    # Look for the key containing SKU data (attributeValues is where SKU-related info is stored)
    attribute_values = product_data.get("attributeValues", [])

    # Loop through each attribute value to extract SKU details
    for item in attribute_values:
        sku_id = item.get("id", "N/A")
        shade = item.get("value", "N/A")
        title = item.get("title", "N/A")
        # Offer price is not found in this response, you may need to fetch it elsewhere
        offer_price = "N/A"  # Replace with real offer price if available in response

        # Store the SKU details in a list of dictionaries
        sku_details.append({
            "skuId": sku_id,
            "shade": shade,
            "offerPrice": offer_price,
            "title": title
        })

    return sku_details


def display_sku_details(sku_details: list) -> None:
    """Display SKU details in the required format."""
    if not sku_details:
        logging.warning("No SKU details found in the response.")
        return

    # Loop through the SKUs and print details
    product_counter = 1  # To track Product number (Product 1, Product 2, etc.)
    for sku in sku_details:
        sku_id = sku.get("skuId", "N/A")
        shade = sku.get("shade", "N/A")
        offer_price = sku.get("offerPrice", "N/A")
        title = sku.get("title", "N/A")

        # Printing output in the required format
        print("--------------------------")
        print(f"Product {product_counter}")
        print(f"skuId : {sku_id}")
        print(f"shade : {shade}")
        print(f"offerPrice : {offer_price}")
        print(f"title : {title}")
        print()  # Blank line between products
        product_counter += 1  # Increment the product counter


def main():
    if len(sys.argv) < 2:
        logging.error("Usage: python coding2.py <product_id>")
        sys.exit(1)

    product_id = sys.argv[1]
    try:
        product_data = fetch_product_details(product_id)
        sku_details = extract_sku_details_from_response(product_data)
        display_sku_details(sku_details)
    except Exception as e:
        logging.error(
            f"Error occurred while processing product ID {product_id}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()