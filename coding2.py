import requests
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

API_BASE_URL = "https://dev.shopalyst.com/shopalyst-service/v1/products/"


def fetch_product_details(product_id: str) -> dict:
    url = f"{API_BASE_URL}{product_id}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch data. Status code: {response.status_code}")
    return response.json()


def get_shade_title_mapping(product_data: dict) -> dict:
    """Map shade ID like 'M423' to full title like 'Lakme Enrich Satin Lipstick - M423'."""
    mapping = {}
    for item in product_data.get("attributeValues", []):
        shade_id = item.get("id")
        title = item.get("title")
        if shade_id and title:
            mapping[shade_id] = title
    return mapping


def display_sku_details(product_data: dict):
    sku_set = product_data.get("skuSet", [])
    title_map = get_shade_title_mapping(product_data)

    if not sku_set:
        logging.warning("No SKU details found.")
        return

    for i, sku in enumerate(sku_set, start=1):
        attributes = sku.get("attributes", {})
        shade_id = attributes.get("1")  # example: "M423"
        shade_title = title_map.get(
            shade_id, f"Title not found for shade {shade_id}")
        offer_price = sku.get("offerPrice", "N/A")
        sku_id = sku.get("skuId", "N/A")

        print("-----------------------------")
        print(f"Product {i}")
        print(f"skuId : {sku_id}")
        print(f"shade : {shade_id}")
        print(f"offerPrice : {offer_price}")
        print(f"title : {shade_title}")
    print("-----------------------------")


def main():
    if len(sys.argv) < 2:
        logging.error("Usage: python script.py <product_id>")
        sys.exit(1)

    product_id = sys.argv[1]
    try:
        product_data = fetch_product_details(product_id)
        display_sku_details(product_data)
    except Exception as e:
        logging.error(f"Error processing product ID {product_id}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()