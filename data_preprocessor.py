import csv
import re
from typing import Tuple

UNITS = ["z", "oz", "ct", "lb", "lbs", "bshl", "l", "bushel", "pint", "gallon", "dozen"]


def clean_raw_catalog(file_path: str) -> list:
    """
    Preprocessing of products in a catalog.
    :param file_path:
    :return:
    """
    with open(file_path, newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        header_row = _clean_header(next(reader))
        number_of_columns = len(header_row)

        return [
            [_clean_product_name(row[0])] + row[1:number_of_columns] for row in reader
        ]


def _clean_header(header_row: list) -> list:
    """
    Remove empty columns from header.
    """
    return [item for item in header_row if item]


def _clean_product_name(product_name: str) -> str:
    """
    Remove quantities and other artifacts from the product names. For future processing,
    those artifacts could be used to enrich data but for the purpose of this exercise, we skip it.
    """
    _, _, _, cleaned_product_name = _get_quantity_from_product_name(product_name)
    cleaned_product_name = _clean_shortcuts(product_name)
    return cleaned_product_name


def _clean_shortcuts(product_name: str) -> str:
    """
    Often shortcuts are used in product names and descriptions. We want to standardize all descriptions/names. It's just
    an example and should be replaced by some general process
    """

    product_name = re.sub(" BRST", " BREAST", product_name)
    product_name = re.sub(" SLCD", " Sliced", product_name)

    return product_name


def _get_quantity_from_product_name(product_name: str) -> Tuple[str, str, str, str]:
    """
    The basic cleaning case:
     - find if there is "Size" in a product name
     - next, check if there is a unit such as Lbs, etc, and a number. Numbers can be provided in many formats like 1/4.
     - at the end check if the given product is sold in "case".
    :param product_name:
    :return: unit of measure, quantity, unit, cleaned product name
    """
    search_result = re.findall(r"(Size \d+)", product_name)
    unit_of_measure, quantity, unit = "", 0, ""
    if search_result:
        unit_of_measure = "each"
        quantity = float(search_result[0].replace("Size ", ""))
        product_name = product_name.replace(search_result[0], "")

    # We are searching for units of measure patterns. Usually, it starts with some digit
    search_result = re.findall(r"([0-9][0-9/.]{0,9} ?[a-zA-Z]{1,6})", product_name)
    if search_result:
        _text = search_result[0].replace(" ", "")
        unit_of_measure = re.findall(r"([a-zA-Z]{1,6})", _text)

        unit_of_measure = (
            unit_of_measure[0] if unit_of_measure[0].lower() in UNITS else ""
        )

        if unit_of_measure:
            quantity = _text.replace(unit_of_measure, "")
            product_name = product_name.replace(search_result[0], "")
            unit = unit_of_measure

    if re.findall(r"(case)", product_name):
        unit_of_measure = "case"
        product_name = re.sub(r"\( ?[cC]ase\)|\(\)", "", product_name)

    return (
        unit_of_measure,
        quantity,
        unit,
        ", ".join([item.strip() for item in product_name.split(",") if item.strip()]),
    )


def clean_order_data(file_path: str) -> list:
    """
    Preprocessing of names of ordered products
    :param file_path: location of csv file with restaurant order
    :return: list of cleaned product names
    """
    with open(file_path, newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        next(reader)  # skip header
        return [
            [_clean_ordered_product_name(row[4])] + row[1:4]
            for row in reader
            if any(row[1:4])
        ]


def _clean_ordered_product_name(product_name: str) -> str:
    cleaned_product_name = _remove_catalog_number(product_name)
    cleaned_product_name = _clean_product_name(cleaned_product_name)
    cleaned_product_name = _clean_artifacts(cleaned_product_name)
    return cleaned_product_name


def _remove_catalog_number(product_name: str) -> str:
    # We could assume some heuristic like catalog number has at least 4 chars and contains at least 1 digit. However
    # for now it just simpler to split the string by few spaces.

    product_name = product_name.split("   ")[0]

    return product_name


def _clean_artifacts(product_name: str) -> str:
    # Next, we have some suppliers like Sysco which do have brand families and some other context-related shortcuts and
    # keywords. For instance Sysco - WHLFCLS (which is wholesome farms) and other like IMPFRSH what can mean a brand or
    # be a shortcut for imported fresh:D or WICHITA which probably is a location of Sysco in Kansas

    product_name = re.sub(
        r"IMPFRSH|WHLFCLS|BELGIO|BBRLIMP|HORMEL|PACKER|WICHITA|HSRCIMP|EMBASSA|BBRLCLS|JDMTCLS|SYSTRNZ|D'ALLAS",
        "",
        product_name,
    )

    return product_name
