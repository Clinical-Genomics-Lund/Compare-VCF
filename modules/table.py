from modules.dataset import Dataset, Variant
import pandas as pd

TopKeysPerDs = dict[str, set[str]]


def write_score_table(
    datasets: list[Dataset], top_n: int, outpath: str, rankmodels: list[str] | None
):
    datasets_w_scores = [ds for ds in datasets if ds.hasScores()]

    (all_top_keys, top_keys_per_ds) = get_top_scored_keys(datasets_w_scores, top_n)
    variant_key = "key"
    top_df = build_data_frame(
        datasets_w_scores, all_top_keys, top_keys_per_ds, top_n, variant_key
    )

    print(top_df)
    # Pull out the ranks strings and add to the top_df
    for key in top_df[variant_key]:
        print(f"Finding {key}")

    top_df.to_csv(outpath, sep="\t", index=False)


def build_data_frame(
    datasets: list[Dataset],
    all_top_keys: set[str],
    top_keys_per_ds: TopKeysPerDs,
    top_n: int,
    key: str,
) -> pd.DataFrame:
    table_dict: dict[str, list[bool | int | str]] = dict()
    table_dict[key] = list(all_top_keys)
    for ds in datasets:
        ds_top_keys = top_keys_per_ds[ds.label]
        ds_cols = get_dataset_columns(ds, all_top_keys, ds_top_keys, top_n)

        for key, col in ds_cols.items():
            assert (
                key not in table_dict.keys()
            ), f"{key} already present in table_dict, among keys: {', '.join(list(table_dict.keys()))}"
            table_dict[key] = col

    top_df = pd.DataFrame(table_dict)
    score_labels = [f"{ds.label}_score" for ds in datasets]
    top_df.sort_values(by=score_labels, inplace=True, ascending=False)
    return top_df


def get_dataset_columns(
    ds: Dataset, all_top_keys: set[str], ds_top_keys: set[str], top_n: int
) -> dict[str, list[bool | int | str]]:
    col_dict = dict()
    # FIXME: Avoid hard-coding, lift this up from this function
    present_label = f"{ds.label}_present"
    col_dict[present_label] = [
        ds.getVariantByKey(key) is not None for key in all_top_keys
    ]
    top_n_label = f"{ds.label}_top{top_n}"
    col_dict[top_n_label] = [key in ds_top_keys for key in all_top_keys]
    score_label = f"{ds.label}_score"
    col_dict[score_label] = [ds.getScoreByKey(key) for key in all_top_keys]
    return col_dict


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
