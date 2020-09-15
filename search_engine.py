from adapters import CatalogRepository


class SearchEngine:
    def __init__(self, connection_string: str = ""):
        self._connection_string = connection_string
        self.__repo = None

    @property
    def repo(self):
        if not self.__repo:
            self.__repo = CatalogRepository(connection_string=self._connection_string)
        return self.__repo

    def search_for_product(self, name, limit=3):
        """
        Search for a product base on a product name. The searching process starts with product classification (not implemented)
        so that we can narrow the search space.
        :param name: a product name
        :param limit: number of similar products to return
        :return:
        """
        products = self.repo.fuzzy_search(name, limit=limit)

        search_result = {"search_phrase": name, "results": []}

        for product in products:
            search_result["results"].append(
                {"name": product[0], "confidence": product[1]}
            )

        return search_result
