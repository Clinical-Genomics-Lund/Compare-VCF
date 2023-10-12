from modules.dataset import Dataset
from configobj import ConfigObj


def get_scores_for_shared_variants(
    ds1: Dataset, ds2: Dataset, top_n: int | None, top_from: str = "first"
) -> list[tuple[str, int, int]]:
    """Given two arrays of variants, identify shared variants"""

    if top_n is None:
        all_keys = ds1.getVariantKeys().union(ds2.getVariantKeys())
    else:
        if top_from == "first":
            all_keys = ds1.getTopScoredVariantKeys(top_n)
        elif top_from == "second":
            all_keys = ds2.getTopScoredVariantKeys(top_n)
        else:
            raise ValueError(
                f"top_from should be either first or second, found {top_from}"
            )

    shared_scores = list()
    for key in all_keys:
        ds1_var = ds1.getVariantByKey(key)
        ds2_var = ds2.getVariantByKey(key)

        if ds1_var is None or ds2_var is None:
            continue

        if ds1_var.score is None or ds2_var.score is None:
            continue

        shared_score = (key, ds1_var.score, ds2_var.score)
        shared_scores.append(shared_score)

    return shared_scores


def get_rankscore_categories(rankmodel_path: str, categories_key: str) -> list[str]:
    config = ConfigObj(rankmodel_path)
    categories_section = config[categories_key]
    categories_keys = categories_section.keys()  # type: ignore
    return categories_keys
