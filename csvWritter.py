import csv


import re
from urllib.parse import urlparse
from pathlib import Path


def create_csv_selected_book(book: list):
    headers = [
        "url",
        "available",
        "PriceIncludingVat",
        "PriceExcludingVat",
        "universal_product_code",
        "category",
        "description",
        "title",
        "image_url",
        "ratings",
    ]

    category = book[0]["category"]

    with open(f"library/{category}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers, delimiter=";")
        writer.writeheader()

        for data in book:
            writer.writerow(data)
