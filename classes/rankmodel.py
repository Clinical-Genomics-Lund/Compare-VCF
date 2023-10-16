from configobj import ConfigObj

CATEGORIES_KEY = "Categories"


class RankModel:
    categories: list[str]

    def __init__(self, filepath: str):
        config = ConfigObj(filepath)
        categories_section = config[CATEGORIES_KEY]
        self.categories = categories_section.keys()  # type: ignore


# def get_rankscore_categories(rank_model: RankModel, categories_key: str) -> list[str]:
#     # config = ConfigObj(rankmodel_path)
#     # categories_section = config[categories_key]
#     categories_keys = categories_section.keys()  # type: ignore
#     return categories_keys
