import scrapping
import csvWritter


if __name__ == "__main__":
    categories: list[str] = scrapping.all_categories()
    for category in [
        "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html",
    ]:
        selected = scrapping.selected_category(category)
        csvWritter.create_csv_selected_book(selected)
