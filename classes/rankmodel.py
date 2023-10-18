from configobj import ConfigObj

CATEGORIES_KEY = "Categories"


class RankModel:
    categories: list[str]

    def __init__(self, filepath: str):
        config = ConfigObj(filepath)
        categories_section = config[CATEGORIES_KEY]
        self.categories = categories_section.keys()  # type: ignore


