from modules.dataset import Dataset, Variant
import pandas as pd


def build_table(datasets: list[Dataset], top_n: int, outpath: str):
    def sort_fn(variant: Variant):
        if variant.rankScore is not None:
            return variant.rankScore
        else:
            return -1

    var_key_tops = set()
    datasets_w_scores = [ds for ds in datasets if ds.hasRankScores()]
    for ds in datasets_w_scores:
        # variant_keys = ds.getVariantKeys()
        # all_variants.update(variant_keys)
        variants = ds.variants
        sorted_variants = sorted(variants, key=sort_fn, reverse=True)
        top_variants = sorted_variants[0:top_n]
        var_keys = [var.getKey() for var in top_variants]
        var_key_tops.update(var_keys)

    table_dict = dict()
    table_dict["key"] = list(var_key_tops)
    # var_is_present: list[list[bool]] = []
    # dataset_scores: list[list[int | None]] = []
    for ds in datasets_w_scores:
        ds_is_present = []
        ds_scores = []
        for key in var_key_tops:
            var = ds.getVariantByKey(key)
            is_present = var is not None
            score = var.rankScore if is_present else None

            ds_is_present.append(is_present)
            ds_scores.append(score)
        table_dict[f"{ds.label}_present"] = ds_is_present
        table_dict[f"{ds.label}_score"] = ds_scores
        # var_is_present.append(ds_is_present)
        # dataset_scores.append(ds_scores)

    # ordered_variants = list(all_variants)

    # variants = dataset.variants

    # sorted_variants = sorted(variants, key=sort_fn, reverse=True)
    # top_sorted = sorted_variants[0:top_n]

    # positions: list[str] = [var.getPosStr() for var in top_sorted]
    # variant_strs: list[str] = [var.getAlleleStr() for var in top_sorted]
    # scores: list[int | None] = [var.rankScore for var in top_sorted]

    # top_df = pd.DataFrame({"pos": positions, "mut": variant_strs, "score": scores})
    top_df = pd.DataFrame(table_dict)
    top_df.sort_values(by=[f"{datasets_w_scores[0].label}_score"])

    top_df.to_csv(outpath, sep="\t", index=False)

    print(table_dict)
