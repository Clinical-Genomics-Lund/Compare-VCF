from modules.dataset import Dataset, Variant
import pandas as pd

TopKeysPerDs = dict[str, set[str]]


def write_score_table(datasets: list[Dataset], top_n: int, outpath: str):
    datasets_w_scores = [ds for ds in datasets if ds.hasScores()]

    (all_top_keys, top_keys_per_ds) = get_top_scored_keys(datasets_w_scores, top_n)
    top_df = build_data_frame(datasets_w_scores, all_top_keys, top_keys_per_ds, top_n)
    top_df.to_csv(outpath, sep="\t", index=False)


# FIXME: Think about how this can be handled more elegantly
def build_data_frame(
    datasets: list[Dataset],
    all_top_keys: set[str],
    top_keys_per_ds: TopKeysPerDs,
    top_n: int,
) -> pd.DataFrame:
    table_dict = dict()
    table_dict["key"] = list(all_top_keys)
    score_labels = list()
    for ds in datasets:
        # ds_is_present = []
        # ds_scores = []
        # ds_among_top = []
        # for key in all_top_keys:
        #     var = ds.getVariantByKey(key)
        #     is_present = var is not None
        #     score = var.score if is_present else None
        #     in_top = key in top_keys_per_ds[ds.label]

        #     ds_is_present.append(is_present)
        #     ds_scores.append(score)
        #     ds_among_top.append(in_top)

        present_label = f"{ds.label}_present"
        table_dict[present_label] = [
            ds.getVariantByKey(key) is not None for key in all_top_keys
        ]
        top_n_label = f"{ds.label}_top{top_n}"
        table_dict[top_n_label] = [
            key in top_keys_per_ds[ds.label] for key in all_top_keys
        ]
        score_label = f"{ds.label}_score"
        table_dict[score_label] = [ds.getScoreByKey(key) for key in all_top_keys]
        # table_dict[f"{ds.label}_present"] = ds_is_present
        # table_dict[f"{ds.label}_top{top_n}"] = ds_among_top
        # table_dict[score_label] = ds_scores
        # score_labels.append(score_label)
    top_df = pd.DataFrame(table_dict)
    top_df.sort_values(by=score_labels, inplace=True, ascending=False)
    return top_df


def get_top_scored_keys(
    datasets: list[Dataset], top_n: int
) -> tuple[set[str], TopKeysPerDs]:
    all_top_keys = set()
    top_keys_per_ds: dict[str, set[str]] = dict()

    def sort_fn(variant: Variant):
        if variant.score is not None:
            return variant.score
        else:
            return -1

    for ds in datasets:
        variants = ds.variants
        sorted_variants = sorted(variants, key=sort_fn, reverse=True)
        top_variants = sorted_variants[0:top_n]
        var_keys = [var.getKey() for var in top_variants]
        all_top_keys.update(var_keys)
        top_keys_per_ds[ds.label] = set(var_keys)
    return (all_top_keys, top_keys_per_ds)
