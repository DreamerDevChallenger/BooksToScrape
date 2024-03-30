import csv


import os
from urllib.parse import urlparse
from pathlib import Path


def create_csv_selected_book(book: list):
    headers = [
        "url",
        "available",
        "price_including_vat",
        "price_excluding_vat",
        "universal_product_code",
        "category",
        "description",
        "title",
        "image_url",
        "ratings",
    ]

    category = book[0]["category"]

    if not os.path.exists(f"library"):
        os.makedirs(f"library")

    with open(f"library/{category}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers, delimiter=";")
        writer.writeheader()

        for data in book:
            writer.writerow(data)
