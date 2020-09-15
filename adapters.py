"""
This module is an adapter to a repository in which we store a products catalog. We assume that an interface of this
the repository has a Levenshtein distance search method implemented or other fuzzy search methods.
In addition, we assume that this repository is a flat-file and querying is just looping over all elements.
"""
from fuzzywuzzy import fuzz, process

from config import CATALOG_LOCATION
from data_preprocessor import clean_raw_catalog


class CatalogRepository:
    __pointer = None

    def __init__(self, connection_string=""):
        self._connection_string = connection_string

    def connect(self):
        file_path = self._connection_string or CATALOG_LOCATION
        return clean_raw_catalog(file_path)

    @property
    def pointer(self):
        if not self.__pointer:
            self.__pointer = self.connect()

        return self.__pointer

    def fuzzy_search(self, name: str, limit=3, scorer=None) -> list:
        choices = self.get_catalog_names()
        if not scorer:
            scorer = fuzz.token_set_ratio
        return process.extract(name, choices, limit=limit, scorer=scorer)

    def get_catalog_names(self):
        return [row[0] for row in self.pointer]
