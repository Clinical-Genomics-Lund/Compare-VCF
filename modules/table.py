from modules.dataset import Dataset, Variant
import pandas as pd


def build_table(datasets: list[Dataset], top_n: int, outpath: str):
    def sort_fn(variant: Variant):
        if variant.rankScore is not None:
            return variant.rankScore
        else:
            return -1

    all_top_keys = set()
    top_keys_per_ds: dict[str, set[str]] = dict()

    datasets_w_scores = [ds for ds in datasets if ds.hasRankScores()]
    for ds in datasets_w_scores:
        # variant_keys = ds.getVariantKeys()
        # all_variants.update(variant_keys)
        variants = ds.variants
        sorted_variants = sorted(variants, key=sort_fn, reverse=True)
        top_variants = sorted_variants[0:top_n]
        var_keys = [var.getKey() for var in top_variants]
        all_top_keys.update(var_keys)
        top_keys_per_ds[ds.label] = set(var_keys)

    table_dict = dict()
    table_dict["key"] = list(all_top_keys)
    score_labels = list()
    # var_is_present: list[list[bool]] = []
    # dataset_scores: list[list[int | None]] = []
    for ds in datasets_w_scores:
        ds_is_present = []
        ds_scores = []
        ds_among_top = []
        for key in all_top_keys:
            var = ds.getVariantByKey(key)
            is_present = var is not None
            score = var.rankScore if is_present else None
            in_top = key in top_keys_per_ds[ds.label]

            ds_is_present.append(is_present)
            ds_scores.append(score)
            ds_among_top.append(in_top)
        table_dict[f"{ds.label}_present"] = ds_is_present
        table_dict[f"{ds.label}_top{top_n}"] = ds_among_top
        score_label = f"{ds.label}_score"
        table_dict[score_label] = ds_scores
        score_labels.append(score_label)

    # ordered_variants = list(all_variants)

    # variants = dataset.variants

    # sorted_variants = sorted(variants, key=sort_fn, reverse=True)
    # top_sorted = sorted_variants[0:top_n]

    # positions: list[str] = [var.getPosStr() for var in top_sorted]
    # variant_strs: list[str] = [var.getAlleleStr() for var in top_sorted]
    # scores: list[int | None] = [var.rankScore for var in top_sorted]

    # top_df = pd.DataFrame({"pos": positions, "mut": variant_strs, "score": scores})
    top_df = pd.DataFrame(table_dict)
    print(top_df)
    print(score_labels)
    top_df.sort_values(by=score_labels, inplace=True, ascending=False)
    print(top_df)

    top_df.to_csv(outpath, sep="\t", index=False)
