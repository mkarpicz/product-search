"""
Perform a fuzzy search of ordered products.

Example usage
python3.8 main.py --order-file "data/restaurant-order-table.csv" --output-file "output.json"
python3.8 main.py --order-file "data/restaurant-order-table.csv" --output-file "output.json" --catalog-file "~/Downloads/catalog.csv"

python3.8 main.py --search-phrase "Micro Greens Arrugala"

If output file is not provided the search result will be printed to stdout
"""

import argparse
import json
import pprint
import time

from data_preprocessor import clean_order_data
from search_engine import SearchEngine


def get_ordered_products_names(file_path: str):
    ordered_products = clean_order_data(file_path)
    return [product[0] for product in ordered_products]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--order-file",
        help="A location of a CSV file with an order.",
        dest="order_file",
        default="",
    )
    parser.add_argument(
        "--catalog-file",
        help="A location of a CSV file with products catalog. If not provided defaults to catalog from config file.",
        dest="catalog_file",
        default="",
    )
    parser.add_argument(
        "--output-file",
        help="A location of an output JSON file. If not provided result will be printed to a console.",
        dest="output_file",
        default="",
    )
    parser.add_argument(
        "--search-phrase",
        help="A search phrase to query against products catalog.",
        dest="search_phrase",
        default="",
    )

    args = parser.parse_args()

    if not args.search_phrase and not args.order_file:
        print("Provide search phrase or order file")
        quit()

    if args.order_file:
        product_names = get_ordered_products_names(args.order_file)
    else:
        product_names = [args.search_phrase]

    search_engine = SearchEngine(connection_string=args.catalog_file)
    _start_time = time.time()
    results = [
        search_engine.search_for_product(product_name) for product_name in product_names
    ]
    _elapsed_time = time.time() - _start_time

    if args.output_file:
        with open(args.output_file, "w") as output:
            output.write(json.dumps(results))
    else:
        pprint.pprint(results)

    print("Search results obtained in: {}s".format(_elapsed_time))
