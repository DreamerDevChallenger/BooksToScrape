import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pathlib import Path
import re
import os


def all_categories():
    list = []

    response = requests.get("https://books.toscrape.com/index.html")
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        useless = "catalogue/category/books_1/index.html"

        sidebar = soup.find("div", class_="side_categories").find_all("a")
        for item in sidebar:
            href = item.get("href")
            if not href == useless:
                list.append(f"https://books.toscrape.com/{href}")
    return list


def selected_category(url: str):
    next = next_pages(url)
    data = []

    for url_next in next:
        response = requests.get(url_next)

        if response.status_code == 200:
            page = response.content
            soup = BeautifulSoup(page, "html.parser")
            product = soup.find_all("article", class_="product_pod")

            for link in product:
                href: str = (
                    link.find("a")
                    .get("href")
                    .replace("../../../", "https://books.toscrape.com/catalogue/")
                )
                data.append(selected_book(href))

    return data


def next_pages(url):

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        all_data = [url]
        number = 2
        url_replace = url.replace("index.html", "")

        next = soup.find("li", class_="next")

        if not next == None:
            next_href = next.find("a").get("href")
            all_data.append(f"{url_replace}{next_href}")

            while True:
                url_page = f"{url_replace}page-{number}.html"

                response_next = requests.get(url_page)

                if response_next.status_code == 200:
                    soup_next = BeautifulSoup(response_next.content, "html.parser")
                    next_page = soup_next.find("li", class_="next")

                    if not next_page == None:
                        next_page_href = next_page.find("a").get("href")
                        all_data.append(f"{url_replace}{next_page_href}")
                        number += 1
                    else:
                        break
    return all_data


def selected_book(url):
    response = requests.get(url)

    if response.status_code == 200:
        page = response.content
        soup = BeautifulSoup(page, "html.parser")

        title = soup.find("h1").string

        links = soup.find_all("a")

        category = []

        for link in links:
            href = link.get("href")
            if "category/books/" in href:
                category.append(link.text)

        number_available = (
            soup.find("table", class_="table-striped")
            .find("th", string="Availability")
            .find_next_sibling("td")
            .string.replace("In stock (", "")
            .replace(" available)", "")
        )

        universal_product_code = (
            soup.find("table", class_="table-striped")
            .find("th", string="UPC")
            .find_next_sibling("td")
            .string
        )

        price_excluding_vat = (
            soup.find("table", class_="table-striped")
            .find("th", string="Price (excl. tax)")
            .find_next_sibling("td")
            .string
        )

        price_including_vat = (
            soup.find("table", class_="table-striped")
            .find("th", string="Price (incl. tax)")
            .find_next_sibling("td")
            .string
        )

        ratings = (
            soup.find("div", class_="product_main")
            .find("p", class_="star-rating")
            .get("class")[1]
        )

        image_url = (
            soup.find("div", id="product_gallery")
            .find("img")
            .get("src")
            .replace("../../", "http://books.toscrape.com/")
        )

        description = ""

        try:
            description = (
                soup.find("div", id="product_description").find_next_sibling("p").string
            )
        except:
            description = "N/A"

        download_image(image_url, category[0], title)

        book = {
            "url": response.url,
            "universal_product_code": universal_product_code,
            "title": title,
            "price_including_vat": price_including_vat,
            "price_excluding_vat": price_excluding_vat,
            "available": int(number_available),
            "category": category[0],
            "ratings": ratings,
            "image_url": image_url,
            "description": description,
        }

        print(f"{title} success")

        return book


def download_image(url, category, title):
    # Create folder if it doesn't exist
    if not os.path.exists(f"image/{category}"):
        os.makedirs(f"image/{category}")

    file_extension = get_extension(url)
    file_title = clean_title(title)
    image_path = os.path.join(f"image/{category}", file_title + file_extension)

    response = requests.get(url)

    if response.status_code == 200:
        with open(image_path, "wb") as f:
            f.write(response.content)
        print(f"Image downloaded successfully: {file_title}")
    else:
        print(f"Failed to download image from {url}")


def clean_title(title):
    cleaned_title = re.sub(r"[^\w\s-]", "", title)
    cleaned_title = cleaned_title.replace(" ", "_")
    return cleaned_title[:50]


def get_extension(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    ext = Path(path).suffix
    return ext
