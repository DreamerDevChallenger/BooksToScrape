import scrapping
import csvWritter


if __name__ == "__main__":
    categories: list[str] = scrapping.all_categories()
    for category in categories:
        selected = scrapping.selected_category(category)
        csvWritter.create_csv_selected_book(selected)
